from enum import auto

from fastapi_utils.enums import StrEnum


class ComponentCategory(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    Generator = auto()
    Load = auto()
    Battery = auto()
    Interconnector = auto()
