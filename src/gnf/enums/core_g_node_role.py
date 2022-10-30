from enum import auto

from fastapi_utils.enums import StrEnum


class CoreGNodeRole(StrEnum):
    @classmethod
    def values(cls):
        return [elt.value for elt in cls]

    ConductorTopologyNode = auto()
    AtomicTNode = auto()
    TerminalAsset = auto()
    InterconnectionComponent = auto()
    Other = auto()
    MarketMaker = auto()
    AtomicMeteringNode = auto()
