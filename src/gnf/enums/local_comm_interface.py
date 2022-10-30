from enum import auto

from fastapi_utils.enums import StrEnum


class LocalCommInterface(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    ANALOG_4_20_MA = auto()
    RS232 = auto()
    I2C = auto()
    WIFI = auto()
    SIMRABBIT = auto()
    UNKNOWN = auto()
    ETHERNET = auto()
    ONEWIRE = auto()
    RS485 = auto()
