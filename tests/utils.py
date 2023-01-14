import time
from typing import Callable
from typing import NamedTuple
from typing import Optional

from gnf.actor_base import ActorBase
from gnf.actor_base import OnSendMessageDiagnostic
from gnf.config import VanillaSettings
from gnf.enums import RegistryGNodeRole
from gnf.types import HeartbeatA
from gnf.types import HeartbeatA_Maker


def wait_for(
    f: Callable[[], bool],
    timeout: float,
    tag: str = "",
    raise_timeout: bool = True,
    retry_duration: float = 0.1,
) -> bool:
    """Call function f() until it returns True or a timeout is reached. retry_duration specified the sleep time between
    calls. If the timeout is reached before f return True, the function will either raise a ValueError (the default),
    or, if raise_timeout==False, it will return False. Function f is guaranteed to be called at least once. If an
    exception is raised the tag string will be attached to its message.
    """
    now = time.time()
    until = now + timeout
    if now >= until:
        if f():
            return True
    while now < until:
        if f():
            return True
        now = time.time()
        if now < until:
            time.sleep(min(retry_duration, until - now))
            now = time.time()
    if raise_timeout:
        raise ValueError(
            f"ERROR. Function {f} timed out after {timeout} seconds. {tag}"
        )
    else:
        return False


class GNodeFactoryRabbitStubRecorder(ActorBase):
    messages_received: int
    messages_routed_internally: int
    latest_from_g_node_role_value: Optional[str]
    latest_from_g_node_alias: Optional[str]
    latest_payload: Optional[HeartbeatA]
    routing_to_gnr__heartbeat_a__worked: bool = False

    def __init__(self, settings: VanillaSettings):
        self.messages_received = 0
        self.messages_routed_internally = 0
        self.latest_from_g_node_role_value: Optional[str] = None
        self.latest_from_g_node_alias: Optional[str] = None
        self.latest_payload: Optional[HeartbeatA] = None

        super().__init__(settings=settings, g_node_type_short_alias="gnf")

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        self.messages_received += 1
        super().on_message(_unused_channel, basic_deliver, properties, body)

    def route_direct_message(
        self, from_g_node_role_value: str, from_g_node_alias: str, payload: HeartbeatA
    ):
        self.messages_routed_internally += 1
        self.latest_payload = payload
        self.latest_from_g_node_role_value = from_g_node_role_value
        self.latest_from_g_node_alias = from_g_node_alias
        if isinstance(payload, HeartbeatA):
            pass
        if from_g_node_role_value == RegistryGNodeRole.G_NODE_REGISTRY.value:
            self.gnr__heartbeat_a__received(from_g_node_alias, payload)

    def prepare_for_death(self):
        self.actor_main_stopped = True

    def gnr__heartbeat_a__received(self, from_g_node_alias: str, payload: HeartbeatA):
        self.routing_to_gnr__heartbeat_a__worked = True

    def summary_str(self):
        """Summarize results in a string"""
        return (
            f"AbstractActor [{self.alias}] messages_received: {self.messages_received}  "
            f"latest_payload: {self.latest_payload}"
        )
