"""heartbeat.a.100 type"""

from errors import SchemaError
from schemata.heartbeat_a_base import HeartbeatABase


class HeartbeatA(HeartbeatABase):
    def check_for_errors(self):
        errors = self.derived_errors() + self.hand_coded_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making heartbeat.a.100 for {self}: {errors}")

    def hand_coded_errors(self):
        return []
