from enum import auto

from fastapi_utils.enums import StrEnum


class Unit(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    Fahrenheit = auto()
    AmpsRms = auto()
    Celcius = auto()
    Wh = auto()
    VoltsRms = auto()
    Gpm = auto()
    W = auto()
    Unitless = auto()
