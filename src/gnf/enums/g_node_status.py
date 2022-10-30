from enum import auto

from fastapi_utils.enums import StrEnum


class GNodeStatus(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    PermanentlyDeactivated = auto()
    Pending = auto()
    Active = auto()
    Suspended = auto()
