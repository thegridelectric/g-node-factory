import enum
import functools
import json
import logging
import threading
import time
import traceback
import uuid
from abc import ABC
from abc import abstractmethod
from tkinter import ON
from typing import Dict
from typing import Optional

import api_types
import pendulum
import pika
import property_format
import utils
from config import GnfSettings
from enums.registry_g_node_role_map import RegistryGNodeRole
from errors import SchemaError
from schemata.heartbeat_a_maker import HeartbeatA


class RegistryGNodeRoleShortAlias(enum.Enum):
    GNF = "gnf"
    GNR = "gnr"
    GW = "gw"
    WC = "wc"
    WIR = "wir"


RoleByShortAlias: Dict[RegistryGNodeRoleShortAlias, RegistryGNodeRole] = {
    RegistryGNodeRoleShortAlias.GNF: RegistryGNodeRole.G_NODE_FACTORY,
    RegistryGNodeRoleShortAlias.GNR: RegistryGNodeRole.G_NODE_REGISTRY,
    RegistryGNodeRoleShortAlias.GW: RegistryGNodeRole.GRID_WORKS,
    RegistryGNodeRoleShortAlias.WC: RegistryGNodeRole.WORLD_COORDINATOR,
    RegistryGNodeRoleShortAlias.WIR: RegistryGNodeRole.WORLD_INSTANCE_REGISTRY,
}


class RoutingKeyType(enum.Enum):
    JSON_DIRECT_MESSAGE = "json"
    JSON_BROADCAST = "jsonb"
    GW_MQTT = "mqtt"
    GW_SERIAL = "s"
    GW_PUBSUB = "pubsub"


class OnSendMessageDiagnostic(enum.Enum):
    CHANNEL_NOT_OPEN = "ChannelNotOpen"
    STOPPED_SO_NOT_SENDING = "StoppedSoNotSending"
    STOPPING_SO_NOT_SENDING = "StoppingSoNotSending"
    MESSAGE_SENT = "MessageSent"
    UNKNOWN_ERROR = "UnknownError"


class OnReceiveMessageDiagnostic(enum.Enum):
    TYPE_NAME_DECODING_PROBLEM = "TypeNameDecodingProblem"
    UNKNOWN_ROUTING_KEY_TYPE = "UnknownRoutingKeyType"
    UNHANDLED_ROUTING_KEY_TYPE = "UnhandledRoutingKeyType"
    UNKNOWN_TYPE_NAME = "UnknownTypeName"
    FROM_GNODE_DECODING_PROBLEM = "FromGNodeDecodingProblem"
    UNKONWN_GNODE = "UnknownGNode"
    TO_DIRECT_ROUTING = "ToDirectRouting"


BACKOFF_NUMBER = 16

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.WARNING)


class ActorBase(ABC):
    SHUTDOWN_INTERVAL = 0.1

    def __init__(
        self,
        g_node_type_short_alias: str,
        settings: GnfSettings,
    ):
        self.settings = settings
        self.agent_shutting_down_part_one = False
        self.alias = settings.algo.gnf_g_node_alias
        self.g_node_type_short_alias = g_node_type_short_alias
        self.actor_main_stopped = False

        adder = "-F" + str(uuid.uuid4()).split("-")[0][0:3]
        self.queue_name = self.alias + adder
        self._consume_exchange = g_node_type_short_alias + "_tx"
        self._publish_exchange = g_node_type_short_alias + "mic_tx"

        self._consume_connection: Optional[
            pika.adapters.select_connection.SelectConnection
        ] = None
        self._consume_channel: Optional[pika.channel.Channel] = None
        self._closing_consumer = False
        self._consumer_tag = None
        self.should_reconnect_consumer = False
        self.was_consuming = False
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1
        self._reconnect_delay = 0
        self._url = self.settings.rabbit.url.get_secret_value()

        self.rmq_consumer = ""
        self.result = None
        self.created_at = pendulum.now().in_timezone("UTC")
        self.is_debug_mode = False
        self.old_consume_connections = []
        self.consuming_thread = threading.Thread(target=self.run_reconnecting_consumer)
        self.publishing_thread = None  # set up after consumer is all done
        self._publish_connection: Optional[
            pika.adapters.select_connection.SelectConnection
        ] = None
        self._publish_channel: Optional[pika.channel.Channel] = None
        self._stopping = False
        self._stopped = True
        self.old_publish_connections = []
        self._latest_on_message_diagnostic: Optional[OnReceiveMessageDiagnostic] = None

    def start(self):
        self.consuming_thread.start()
        self._stopped = False

    def stop(self):
        self.commence_shutting_down()
        while self.actor_main_stopped is False:
            time.sleep(self.SHUTDOWN_INTERVAL)
        self.stop_publisher()
        self.stop_consumer()
        self.consuming_thread.join()
        self.publishing_thread.join()
        self._stopping = False
        self._stopped = True

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. If a message
        does not get here that you expect should get here, check the routing key
        of the outbound message and the rabbitmq bindings.

        Parses the TypeName of the message payload and the GNodeAlias of the sender.
        If it recognizes the GNode and the TypeName then it sends the message on to
        the check_routing function, which will be defined in a child class (e.g., the
        GNodeFactoryActorBase if the actor is a GNodeFactory).

        From RabbitMQ:  The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body
        """

        LOGGER.info(
            f"In actor_base on_message. Got {basic_deliver.routing_key} with delivery tag {basic_deliver.delivery_tag}"
        )
        self.acknowledge_message(basic_deliver.delivery_tag)
        try:
            type_name = self.get_payload_type_name(basic_deliver, body)
        except SchemaError:
            return

        if type_name not in api_types.get_api_type_name_list():
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.UNKNOWN_TYPE_NAME
            )
            LOGGER.info(
                f"IGNORING MESSAGE. {self._latest_on_message_diagnostic}: {type_name}"
            )
            return

        try:
            payload_as_tuple = api_types.TypeMakerByName[type_name].type_to_tuple(body)
        except Exception as e:
            LOGGER.warning(
                f"TypeName for incoming message claimed to be {type_name}, but was not true! Failed to make a {api_types.TypeMakerByName[type_name].tuple}"
            )
            return

        routing_key: str = basic_deliver.routing_key

        try:
            from_g_node_alias = self.from_g_node_alias_from_routing_key(routing_key)
        except SchemaError as e:
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.FROM_GNODE_DECODING_PROBLEM
            )
            LOGGER.info(f"IGNORING MESSAGE. {self._latest_on_message_diagnostic}: {e}")
            return
        try:
            from_g_node_role_value = self.from_g_node_type_name_from_routing_key(
                routing_key
            )
        except SchemaError as e:
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.FROM_GNODE_DECODING_PROBLEM
            )
            LOGGER.info(f"IGNORING MESSAGE. {self._latest_on_message_diagnostic}: {e}")
            return

        self._latest_on_message_diagnostic = (
            OnReceiveMessageDiagnostic.TO_DIRECT_ROUTING
        )
        self.route_direct_message(
            from_g_node_role_value=from_g_node_role_value,
            from_g_node_alias=from_g_node_alias,
            payload=payload_as_tuple,
        )

    def send_direct_message(
        self, payload: HeartbeatA, to_g_node_type_short_alias: str, to_g_node_alias: str
    ) -> OnSendMessageDiagnostic:
        """Publish a direct message to another GNode in the registry world. The only type
        of direct messages in the registry use json (i.e. no more streamlined serial encoding),
        unlike in non-registry worlds.

        Args:
            payload: Any GridWorks schemata with a json content-type
            that includes TypeName as a json key, and has as_type()
            as an encoding method.
            to_g_node_type_short_alias (str): gnf, gnr, gw, wc or wir. To be replaced
            when the GNode data class is working
            to_g_node_alias (str): The GNodeAlias of the message recipient, in
            LRD format. To be replaced when the GNode data class is workgin.
            correlation_id (int, optional): Defaults to 1. Can be used for debugging.

        Returns:
            OnSendMessageDiagnostic: MESSAGE_SENT with success, otherwise some
            description of why the message was not sent.
        """

        if self._stopping:
            return OnSendMessageDiagnostic.STOPPING_SO_NOT_SENDING
        if self._stopped:
            return OnSendMessageDiagnostic.STOPPED_SO_NOT_SENDING

        routing_key = self.direct_routing_key(
            to_g_node_type_short_alias=to_g_node_type_short_alias,
            to_g_node_alias=to_g_node_alias,
        )

        if "MessageId" in payload._asdict():
            correlation_id = payload.MessageId
        else:
            correlation_id = str(uuid.uuid4())

        properties = pika.BasicProperties(
            reply_to=self.queue_name,
            app_id=self.alias,
            type=RoutingKeyType.JSON_DIRECT_MESSAGE.value,
            correlation_id=correlation_id,
        )

        if self._publish_channel is None:
            LOGGER.error(f"No publish channel so not sending {routing_key}")
            return OnSendMessageDiagnostic.CHANNEL_NOT_OPEN
        if not self._publish_channel.is_open:
            LOGGER.error(f"Publish channel not open so not sending {routing_key}")
            return OnSendMessageDiagnostic.CHANNEL_NOT_OPEN

        try:
            self._publish_channel.basic_publish(
                exchange=self._publish_exchange,
                routing_key=routing_key,
                body=payload.as_type(),
                properties=properties,
            )
            LOGGER.info(f" [x] Sent {payload.TypeName} w routing key {routing_key}")
            return OnSendMessageDiagnostic.MESSAGE_SENT

        except BaseException as err:
            LOGGER.error("Problem w publish channel")
            LOGGER.error(traceback.format_exc())
            LOGGER.error(f"{err.args}")
            return OnSendMessageDiagnostic.UNKNOWN_ERROR

    #####################
    # Abstract methods
    #####################

    @abstractmethod
    def route_direct_message(self, from_g_node_alias: str, payload: HeartbeatA):
        raise NotImplementedError

    @abstractmethod
    def prepare_for_death(self):
        """Once the agent is ready for its comms to be shut down it sets
        actor_main_stopped  to True. Write stoic code, with your
        agents ready for death at all times.  However, if there are threads running
        beyond the two designed for publishing and consuming messages, shut those
        down in this method."""
        raise NotImplementedError

    ########################
    # Core Rabbit infrastructure
    ########################

    def on_rabbit_infrastructure_ready(self):
        pass

    def flush_consumer(self):
        self.should_reconnect_consumer = False
        self.was_consuming = False
        self._consume_connection = None
        self._consume_channel = None
        self._closing_consumer = False
        self._consumer_tag = None
        self._consuming = False

    def run_reconnecting_consumer(self):
        while not self.actor_main_stopped:
            self.run_consumer()
            self._maybe_reconnect_consumer()

    def _maybe_reconnect_consumer(self):
        if self.should_reconnect_consumer:
            self.stop_consumer()
            reconnect_delay = self._get_reconnect_delay()
            if not self.actor_main_stopped:
                LOGGER.info("Reconnecting after %d seconds", reconnect_delay)
            time.sleep(reconnect_delay)
            self.flush_consumer()

    def _get_reconnect_delay(self):
        if self.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay

    def connect_consumer(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_consumer_connection_open method
        will be invoked by pika.
        :rtype: pika.SelectConnection
        """
        LOGGER.info("Connecting to %s", self._url)
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_consumer_connection_open,
            on_open_error_callback=self.on_consumer_connection_open_error,
            on_close_callback=self.on_consumer_connection_closed,
        )

    def close_consumer_connection(self):
        self._consuming = False
        if self._consume_connection:
            if (
                not self._consume_connection.is_closing
                and not self._consume_connection.is_closed
            ):
                LOGGER.info("Closing consume connection")
                self._consume_connection.close()

    def on_consumer_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.
        :param pika.SelectConnection _unused_connection: The connection
        """
        LOGGER.info("Connection opened")
        self.open_consume_channel()

    def on_consumer_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """
        LOGGER.error(f"Consumer connection open failed: {err}")
        self.reconnect_consumer()

    def on_consumer_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.
        """
        self._consume_channel = None
        if self._closing_consumer:
            self._consume_connection.ioloop.stop()
        else:
            LOGGER.warning(f"Consumer connection closed, reconnect necessary: {reason}")
            self.reconnect_consumer()

    def reconnect_consumer(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        self.should_reconnect_consumer = True
        self.stop_consumer()

    def open_consume_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """
        LOGGER.info("Creating a new channel")
        self._consume_connection.channel(on_open_callback=self.on_consumer_channel_open)

    def on_consumer_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.
        Since the channel is now open, we'll declare the exchange to use.
        :param pika.channel.Channel channel: The channel object
        """
        LOGGER.info("Channel opened")
        self._consume_channel = channel
        self.add_on_consume_channel_close_callback()
        self.setup_exchange()

    def add_on_consume_channel_close_callback(self):
        """This method tells pika to call the on_consumer_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        LOGGER.info("Adding consumer channel close callback")
        self._consume_channel.add_on_close_callback(self.on_consumer_channel_closed)

    def on_consumer_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.
        :param pika.channel.Channel: The closed channel
        :param Exception reason: why the channel was closed
        """
        LOGGER.warning("Consume channel %i was closed: %s", channel, reason)
        self.close_consumer_connection()

    def setup_exchange(self):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.
        :param str|unicode exchange_name: The name of the exchange to declare
        """
        LOGGER.info("Declaring exchange: %s", self._consume_exchange)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(
            self.on_exchange_declareok, userdata=self._consume_exchange
        )
        self._consume_channel.exchange_declare(
            exchange=self._consume_exchange,
            exchange_type="topic",
            durable=True,
            internal=True,
            callback=cb,
        )

    def on_exchange_declareok(self, _unused_frame, userdata):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.
        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param str|unicode userdata: Extra user data (exchange name)
        """
        LOGGER.info("Exchange declared: %s", userdata)
        self.setup_queue(self.queue_name)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        :param str|unicode queue_name: The name of the queue to declare.
        """
        LOGGER.info(f"Declaring queue {self.queue_name}")
        cb = functools.partial(self.on_queue_declareok)
        self._consume_channel.queue_declare(
            queue=self.queue_name, auto_delete=True, callback=cb
        )

    def on_queue_declareok(self, _unused_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.
        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        lru_alias = utils.dot_to_underscore(self.alias)

        direct_message_to_me_binding = f"*.*.*.*.{lru_alias}"

        LOGGER.info(
            "Binding %s to %s with %s",
            self._consume_exchange,
            self.queue_name,
            direct_message_to_me_binding,
        )
        cb = functools.partial(
            self.on_direct_message_bindok, binding=direct_message_to_me_binding
        )
        self._consume_channel.queue_bind(
            self.queue_name,
            self._consume_exchange,
            routing_key=direct_message_to_me_binding,
            callback=cb,
        )

    def on_direct_message_bindok(self, _unused_frame, binding):
        """Invoked by pika when the Queue.Bind method has completed for direct messages. At this
        point we will set the prefetch count for the channel.
        :param pika.frame.Method _unused_frame: The Queue.BindOk response frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        LOGGER.info(f"Queue {self.queue_name} bound with {binding}")
        self.set_qos()

    def set_qos(self):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.
        """
        self._consume_channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok
        )

    def on_basic_qos_ok(self, _unused_frame):
        """Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.
        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame
        """
        LOGGER.info("QOS set to: %d", self._prefetch_count)
        self.additional_rabbit_stuff_after_rabbit_base_setup_is_done()
        self.start_consuming()
        self.publishing_thread = threading.Thread(target=self.run_publisher)
        self.publishing_thread.start()

    def additional_rabbit_stuff_after_rabbit_base_setup_is_done(self):
        pass

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_consumer_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """
        LOGGER.info("Issuing consumer related RPC commands")
        self.add_on_cancel_consumer_callback()
        self._consumer_tag = self._consume_channel.basic_consume(
            self.queue_name, self.on_message
        )
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_consumer_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.
        """
        LOGGER.info("Adding consumer cancellation callback")
        self._consume_channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.
        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """
        LOGGER.info("Consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._consume_channel:
            self._consume_channel.close()

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.
        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        """
        LOGGER.debug(
            f"Acknowledging message {delivery_tag}",
        )
        self._consume_channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._consume_channel:
            LOGGER.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            cb = functools.partial(
                self.on_cancelconsumer_ok, userdata=self._consumer_tag
            )
            self._consume_channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelconsumer_ok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_consumer_channel_closed method once the channel has been
        closed, which will in-turn close the connection.
        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)
        """
        self._consuming = False
        LOGGER.info(
            "RabbitMQ acknowledged the cancellation of the consumer: %s", userdata
        )
        self.close_consumer_channel()
        self._closing_consumer = False

    def close_consumer_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        if self._consume_channel:
            if (
                not self._consume_channel.is_closing
                and not self._consume_channel.is_closed
            ):
                self._consume_channel.close()

    def run_consumer(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """

        self._consume_connection = self.connect_consumer()
        self._consume_connection.ioloop.start()

    def stop_consumer(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelconsumer_ok
        will be invoked by pika, which will then closing the channel and
        connection. If you want to use this with CTRL-C, figure out
        how to add back the commented out ioloop.start() below without error.
        """
        if not self._closing_consumer:
            self._closing_consumer = True
            LOGGER.info("Consumer connection stopping")
            if self._consuming:
                self.stop_consuming()
                # self._consume_connection.ioloop.start()
            else:
                self._consume_connection.ioloop.stop()

            LOGGER.info("Consumer connection stopped")

    def connect_publisher(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.
        :rtype: pika.SelectConnection
        """
        LOGGER.info("Setting up publisher connection to %s", self._url)
        return pika.SelectConnection(
            pika.URLParameters(self._url),
            on_open_callback=self.on_publish_connection_open,
            on_open_error_callback=self.on_publish_connection_open_error,
            on_close_callback=self.on_publish_connection_closed,
        )

    def on_publish_connection_open(self, _unused_connection):
        """This method is called by pika once the publisher connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.
        :param pika.SelectConnection _unused_connection: The connection
        """
        LOGGER.info("Producer connection opened")
        self.open_publish_channel()

    def on_publish_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """
        LOGGER.error("Producer connection open failed, reopening in 1 second: %s", err)
        self._publish_connection.ioloop.call_later(
            1, self._publish_connection.ioloop.stop
        )

    def on_publish_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.
        """
        self._publish_channel = None
        if self._stopping:
            self._publish_connection.ioloop.stop()
        else:
            LOGGER.warning("Connection closed, reopening in 1 second: %s", reason)
            self._publish_connection.ioloop.call_later(
                1, self._publish_connection.ioloop.stop
            )

    def open_publish_channel(self):
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.
        """
        LOGGER.info("Creating a new publish channel")
        self._publish_connection.channel(on_open_callback=self.on_publish_channel_open)

    def on_publish_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.
        Since the channel is now open, we'll declare the exchange to use.
        :param pika.channel.Channel channel: The channel object
        """
        LOGGER.info("Publish channel opened")
        self._publish_channel = channel
        self.on_rabbit_infrastructure_ready()
        self.add_on_publish_channel_close_callback()

    def add_on_publish_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        LOGGER.info("Adding channel close callback")
        self._publish_channel.add_on_close_callback(self.on_publish_channel_closed)

    def on_publish_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.
        :param pika.channel.Channel channel: The closed channel
        :param Exception reason: why the channel was closed
        """
        LOGGER.warning(f"Publish channel {channel} was closed: {reason}")
        self._publish_channel = None
        if not self._stopping:
            self._publish_connection.close()

    def run_publisher(self):
        """Run the example code by connecting and then starting the IOLoop."""
        while not self._stopping:
            self._publish_connection = None
            try:
                self._publish_connection = self.connect_publisher()
                self._publish_connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop_publisher()
                if (
                    self._publish_connection is not None
                    and not self._publish_connection.is_closed
                ):
                    # Finish closing
                    self._publish_connection.ioloop.start()

        LOGGER.info("Stopped")

    def stop_publisher(self):
        """Stop the example by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.
        """
        LOGGER.info(
            "Stopping RabbitMq message production - closing channel and connection"
        )
        self._stopping = True
        self.close_publish_channel()
        self.close_publish_connection()

    def close_publish_channel(self):
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.
        """
        if self._publish_channel:
            if (
                not self._publish_channel.is_closing
                and not self._publish_channel.is_closed
            ):
                self._publish_channel.close()

    def close_publish_connection(self):
        """This method closes the production connection to RabbitMQ."""
        if self._publish_connection:
            if (
                not self._publish_connection.is_closing
                and not self._publish_connection.is_closed
            ):
                self._publish_connection.close()
                LOGGER.info("Closing publish connection")

    ########################
    # Message passing semantics
    ########################

    def get_payload_type_name(self, basic_deliver, body: bytes) -> str:
        """The TypeName tis a string hat provides the strongly typed specification
            (API/ABI) for the incoming message. This is similar to knowing
            the protobuf name/method or the ABI name/method. The list of recognized
            TypeNames is returned by api_types.get_api_type_name_list()

            The TypeName will articulate, in particular, how
            to decode the payload.

        Args:
            basic_deliver: the rabbit basic_deliver object
            body: the rabbit body object (i.e. the payload as incoming type)

        Returns:
            str: raises SchemaError if the TypeName is not accessible.
            Otherwise returns the TypeName

        """
        # TODO: right now we encode this in the routing key. However, we
        # could also add it to a different basic_deliver property, which
        # might be easier for developers to grock.

        try:
            type_name = self.type_name_from_routing_key_and_payload(
                routing_key=basic_deliver.routing_key, payload=body
            )
        except SchemaError as e:
            LOGGER.info(f"Could not figure out TypeName: {e}")
            raise SchemaError(f"{e}")
        return type_name

    def direct_routing_key(
        self, to_g_node_type_short_alias: str, to_g_node_alias: str
    ) -> str:
        msg_type = RoutingKeyType.JSON_DIRECT_MESSAGE.value
        from_alias = utils.dot_to_underscore(self.alias)
        from_role = self.g_node_type_short_alias
        to_role = to_g_node_type_short_alias
        to_alias = utils.dot_to_underscore(to_g_node_alias)
        return f"{msg_type}.{from_alias}.{from_role}.{to_role}.{to_alias}"

    def type_name_from_routing_key_and_payload(
        self, routing_key: str, payload: bytes
    ) -> str:
        """Returns the type alias of the message given the routing key. Raises a SchemaError
        exception if there is a problem decoding the type alias, or if it does not have
        the appropriate left-right-dot format.

        For all the GNode Registry messages, this involves json dumping the payload
        and looking for the TypeName dict key. However, in GridWorks World registries
        where the participating entities represent TerminalAssets, AtomicTNodes, and
        other operational actors in the electric grid model, there are a couple edge patterns
        of routing key where the TypeName is a substring of the routing key itself.

        The decision to embed the routing key INSIDE the body for the main set of
        messages has to do with the length limit of 255 for rabbit routing keys, and
        the desire to include both the FromGNodeAlias and the ToGNodeAlias in that key.

        Args:
            routing_key (str): This is the basic_deliver.routing_key string
            in a rabbit message
            payload (bytes): The body in the on_message

        Returns:
            str: the TypeName of the payload, in left-right-dot format
        """
        routing_key_words = routing_key.split(".")
        try:
            routing_key_type = RoutingKeyType(routing_key_words[0])
        except ValueError:
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.TYPE_NAME_DECODING_PROBLEM
            )
            raise SchemaError(
                f"First  word of {routing_key} not a known RoutingKeyType!"
            )
        if routing_key_type != RoutingKeyType.JSON_DIRECT_MESSAGE:
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.UNHANDLED_ROUTING_KEY_TYPE
            )
            raise SchemaError(
                f"Registry actors only use json type schema, not {routing_key_type} for {routing_key}"
            )
        try:
            payload_as_dict = json.loads(payload)
        except:
            raise SchemaError(
                f"json.loads failed to work for body of {routing_key} message!"
            )
        if "TypeName" not in payload_as_dict.keys():
            raise SchemaError(
                f"TypeName missing as a key in the json dictionary for {routing_key} message!"
            )
        type_name = payload_as_dict["TypeName"]
        try:
            property_format.check_is_lrd_alias_format(type_name)
        except SchemaError:
            self._latest_on_message_diagnostic = (
                OnReceiveMessageDiagnostic.TYPE_NAME_DECODING_PROBLEM
            )
            raise SchemaError(
                f"TypeName {type_name} in {routing_key} message not lrd_alias_format!"
            )
        return type_name

    def from_g_node_alias_from_routing_key(self, routing_key: str) -> str:
        """Returns the GNodeAlias in left-right-dot format. Raises a SchemaError
        if there is trouble getting this.
        Args:
            routing_key (str): This is the basic_deliver.routing_key string
            in a rabbit message
        """
        routing_key_words = routing_key.split(".")
        try:
            from_g_node_alias_lru = routing_key_words[1]
        except:
            raise SchemaError(f"{routing_key} must have at least two words!")
        if not property_format.is_lru_alias_format(from_g_node_alias_lru):
            raise SchemaError(
                f"GNodeAlias not is_lru_alias_format for routing key {routing_key}!"
            )
        from_g_node_alias = utils.underscore_to_dot(from_g_node_alias_lru)
        return from_g_node_alias

    def from_g_node_type_name_from_routing_key(self, routing_key: str) -> str:
        """Returns the RegistryGNodeRole. Raises a SchemaError
        if there is trouble getting this.
        Args:
            routing_key (str): This is the basic_deliver.routing_key string
            in a rabbit message
        """
        routing_key_words = routing_key.split(".")
        try:
            from_g_node_type_short_alias = routing_key_words[2]
        except:
            raise SchemaError(f"{routing_key} must have at least three words!")
        try:
            short_alias = RegistryGNodeRoleShortAlias(from_g_node_type_short_alias)
        except ValueError:
            raise SchemaError(
                f"Unknown short alias {short_alias} in {routing_key}"
                f" Must belong to {RegistryGNodeRoleShortAlias}"
            )

        return RoleByShortAlias[short_alias].value

    #################################################
    # On receiving messages broadcast to all listners
    #################################################

    #################################################
    # Various
    #################################################

    def __repr__(self):
        return f"{self.alias}"

    def screen_print(self, note):
        """Should be replaced by logging"""
        header = f"({pendulum.now('UTC').isoformat()}) {self.alias}: "
        print(header + note)

    def commence_shutting_down(self):
        self.agent_shutting_down_part_one = True
        self.prepare_for_death()