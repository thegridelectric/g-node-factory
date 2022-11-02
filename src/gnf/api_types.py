""" List of all the types used"""
from typing import Dict
from typing import List

from gnf.schemata import BasegnodeCtnCreate_Maker
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import BasegnodeMarketmakerCreate_Maker
from gnf.schemata import BasegnodeOtherCreate_Maker
from gnf.schemata import BasegnodesBroadcast_Maker
from gnf.schemata import BasegnodesGet_Maker
from gnf.schemata import BasegnodeTerminalassetCreate_Maker
from gnf.schemata import DiscoverycertAlgoCreate_Maker
from gnf.schemata import DiscoverycertAlgoTransfer_Maker
from gnf.schemata import HeartbeatA_Maker
from gnf.schemata import OptinTadeedAlgo_Maker
from gnf.schemata import SignandsubmitMtxAlgo_Maker
from gnf.schemata import TadeedAlgoCreate_Maker
from gnf.schemata import TadeedAlgoExchange_Maker
from gnf.schemata import TadeedAlgoTransfer_Maker
from gnf.schemata import TatradingrightsAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoTransfer_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}

type_makers: List[HeartbeatA_Maker] = [
    BasegnodeCtnCreate_Maker,
    BasegnodeGt_Maker,
    BasegnodeMarketmakerCreate_Maker,
    BasegnodeOtherCreate_Maker,
    BasegnodeTerminalassetCreate_Maker,
    BasegnodesBroadcast_Maker,
    BasegnodesGet_Maker,
    DiscoverycertAlgoCreate_Maker,
    DiscoverycertAlgoTransfer_Maker,
    HeartbeatA_Maker,
    OptinTadeedAlgo_Maker,
    SignandsubmitMtxAlgo_Maker,
    TadeedAlgoCreate_Maker,
    TadeedAlgoExchange_Maker,
    TadeedAlgoTransfer_Maker,
    TatradingrightsAlgoCreate_Maker,
    TavalidatorcertAlgoCreate_Maker,
    TavalidatorcertAlgoTransfer_Maker,
]


def version_by_type_name() -> List[str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict = {
        "basegnode.ctn.create": "000",
        "basegnode.gt": "000",
        "basegnode.marketmaker.create": "000",
        "basegnode.other.create": "000",
        "basegnode.terminalasset.create": "000",
        "basegnodes.broadcast": "000",
        "basegnodes.get": "000",
        "discoverycert.algo.create": "000",
        "discoverycert.algo.transfer": "000",
        "heartbeat.a": "000",
        "optin.tadeed.algo": "000",
        "signandsubmit.mtx.algo": "000",
        "tadeed.algo.create": "000",
        "tadeed.algo.exchange": "000",
        "tadeed.algo.transfer": "000",
        "tatradingrights.algo.create": "000",
        "tavalidatorcert.algo.create": "000",
        "tavalidatorcert.algo.transfer": "000",
    }

    return v
