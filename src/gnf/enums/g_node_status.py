from enum import auto

from fastapi_utils.enums import StrEnum


class GNodeStatus(StrEnum):
    Unknown = auto()
    Active = auto()
    Pending = auto()
    PermanentlyDeactivated = auto()
    Suspended = auto()

    @classmethod
    def default(cls) -> "GNodeStatus":
        return cls.Unknown

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]
