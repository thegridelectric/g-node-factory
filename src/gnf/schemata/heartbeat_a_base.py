"""Base for heartbeat.a.100"""
import json
from typing import List
from typing import NamedTuple


class HeartbeatABase(NamedTuple):
    TypeName: str = "heartbeat.a.100"

    def as_type(self) -> bytes:
        return b'{"TypeName": "heartbeat.a.100"}'

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if self.TypeName != "heartbeat.a.100":
            errors.append(
                f"Type requires TypeName of heartbeat.a.100, not {self.TypeName}."
            )

        return errors
