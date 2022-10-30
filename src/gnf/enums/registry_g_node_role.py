from enum import auto

from fastapi_utils.enums import StrEnum


class RegistryGNodeRole(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    GNodeFactory = auto()
    WorldInstanceRegistry = auto()
    WorldCoordinator = auto()
    GNodeRegistry = auto()
    GridWorks = auto()
