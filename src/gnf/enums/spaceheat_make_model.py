from enum import auto

from fastapi_utils.enums import StrEnum


class MakeModel(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    MAGNELAB__SCT0300050 = auto()
    UNKNOWNMAKE__UNKNOWNMODEL = auto()
    OPENENERGY__EMONPI = auto()
    NCD__PR814SPST = auto()
    YMDC__SCT013100 = auto()
    GRIDWORKS__WATERTEMPHIGHPRECISION = auto()
    GRIDWORKS__SIMPM1 = auto()
    GRIDWORKS__SIMCURRENTTRANSFORMER = auto()
    SCHNEIDERELECTRIC__IEM3455 = auto()
    EGAUGE__3010 = auto()
    GRIDWORKS__SIMBOOL30AMPRELAY = auto()
    ADAFRUIT__642 = auto()
    RHEEM__XE50T10H45U0 = auto()
