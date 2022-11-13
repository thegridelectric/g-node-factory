import os

import django
import pika

from gnf.config import BlahBlahBlahSettings

from .utils import GNodeFactoryRabbitStubRecorder
from .utils import GNodeRegistryStubRecorder
from .utils import wait_for


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gnf.settings")
# django.setup()


# def test_pika_types_and_sundry():
#     gnf = GNodeFactoryRabbitStubRecorder(settings=GnfSettings())
#     gnf.start()
#     wait_for(lambda: gnf._consume_connection, 10, "gnf._consume_connection exists")
#     wait_for(lambda: gnf._consuming, 10, "gnf is consuming")
#     wait_for(lambda: gnf._publish_connection.is_open, 10, "gnf publish connection is open")
#     assert gnf._consume_connection.is_open
#     assert gnf._consuming
#     assert gnf._publish_connection.is_open
#     assert isinstance(gnf._publish_connection, pika.adapters.select_connection.SelectConnection)
#     assert isinstance(gnf._consume_connection, pika.adapters.select_connection.SelectConnection)
#     assert isinstance(gnf._publish_channel, pika.channel.Channel)
#     assert isinstance(gnf._consume_channel, pika.channel.Channel)

#     # Sundry:
#     assert repr(gnf) == gnf.settings.g_node_alias
#     gnf.stop()


# def test_sample_routing():
#     gnf = GNodeFactoryRabbitStubRecorder(settings=GnfSettings())
#     gnr = GNodeRegistryStubRecorder(settings=GnfSettings())
#     gnf.start()
#     gnr.start()

#     wait_for(lambda: gnf._consume_connection, 2, "actor._consume_connection exists")
#     wait_for(lambda: gnf._consuming, 2, "actor is consuming")
#     wait_for(lambda: gnf._publish_connection.is_open, 2, "actor publish connection is open")

#     assert gnf.messages_received == 0
#     gnr.send_heartbeat_to_gnf()
#     wait_for(
#         lambda: gnf.routing_to_gnr__heartbeat_a__worked,
#         2,
#         "gnf.routing_to_gnr__heartbeat_a__worked",
#     )
#     assert gnf.routing_to_gnr__heartbeat_a__worked

#     gnr.stop()
#     gnf.stop()
