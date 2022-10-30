from enum import auto

from fastapi_utils.enums import StrEnum


class TelemetryName(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    PowerW = auto()
    WaterTempFTimes1000 = auto()
    GallonsPerMinuteTimes10 = auto()
    WaterFlowGpmTimes100 = auto()
    WaterTempCTimes1000 = auto()
    RelayState = auto()
    Unknown = auto()
    CurrentRmsMicroAmps = auto()
