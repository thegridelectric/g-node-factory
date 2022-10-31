from enum import auto

from fastapi_utils.enums import StrEnum


class RegistryGNodeRole(StrEnum):
    Unknown = auto()
    GNodeFactory = auto()
    GNodeRegistry = auto()
    WorldInstanceRegistry = auto()
    WorldCoordinator = auto()
    GridWorks = auto()

    @classmethod
    def default(cls) -> "RegistryGNodeRole":
        return cls.Unknown

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]
