from enum import auto

from fastapi_utils.enums import StrEnum


class GNodeStatus(StrEnum):
    PermanentlyDeactivated = auto()
    Pending = auto()
    Active = auto()
    Suspended = auto()

    @classmethod
    def default(cls) -> "GNodeStatus":
        return cls.Active
