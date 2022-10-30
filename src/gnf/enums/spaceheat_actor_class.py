from enum import auto

from fastapi_utils.enums import StrEnum


class ActorClass(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    Atn = auto()
    MultipurposeSensor = auto()
    Thermostat = auto()
    BooleanActuator = auto()
    SimpleSensor = auto()
    NoActor = auto()
    HomeAlone = auto()
    PrimaryScada = auto()
    PrimaryMeter = auto()
