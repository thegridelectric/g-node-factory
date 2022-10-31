from enum import auto

from fastapi_utils.enums import StrEnum


class RegistryGNodeRole(StrEnum):
    GNodeFactory = auto()
    WorldInstanceRegistry = auto()
    WorldCoordinator = auto()
    GNodeRegistry = auto()
    GridWorks = auto()

    @classmethod
    def default(cls) -> "RegistryGNodeRole":
        return cls.GridWorks
