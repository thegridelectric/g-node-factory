from enum import auto

from fastapi_utils.enums import StrEnum


class Role(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    BooleanActuator = auto()
    MultipurposeSensor = auto()
    HydronicPipe = auto()
    DedicatedThermalStore = auto()
    Atn = auto()
    RadiatorFan = auto()
    PrimaryScada = auto()
    Outdoors = auto()
    Heatpump = auto()
    HomeAlone = auto()
    PipeFlowMeter = auto()
    CurrentTransformer = auto()
    BoostElement = auto()
    CirculatorPump = auto()
    HeatedSpace = auto()
    RoomTempSensor = auto()
    BaseboardRadiator = auto()
    PipeTempSensor = auto()
    OutdoorTempSensor = auto()
    TankWaterTempSensor = auto()
    PrimaryMeter = auto()
