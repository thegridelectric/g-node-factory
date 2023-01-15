""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gnf.types import BasegnodeCtnCreate_Maker
from gnf.types import BaseGNodeGt_Maker
from gnf.types import BasegnodeMarketmakerCreate_Maker
from gnf.types import BasegnodeOtherCreate_Maker
from gnf.types import BasegnodesBroadcast_Maker
from gnf.types import BasegnodesGet_Maker
from gnf.types import BasegnodeTerminalassetCreate_Maker
from gnf.types import DebugTcReinitializeTime_Maker
from gnf.types import DiscoverycertAlgoCreate_Maker
from gnf.types import DiscoverycertAlgoTransfer_Maker
from gnf.types import GwCertId_Maker
from gnf.types import HeartbeatA_Maker
from gnf.types import InitialTadeedAlgoCreate_Maker
from gnf.types import InitialTadeedAlgoOptin_Maker
from gnf.types import InitialTadeedAlgoTransfer_Maker
from gnf.types import NewTadeedAlgoOptin_Maker
from gnf.types import NewTadeedSend_Maker
from gnf.types import OldTadeedAlgoReturn_Maker
from gnf.types import PauseTime_Maker
from gnf.types import ResumeTime_Maker
from gnf.types import SlaEnter_Maker
from gnf.types import TadeedSpecsHack_Maker
from gnf.types import TatradingrightsAlgoCreate_Maker
from gnf.types import TavalidatorcertAlgoCreate_Maker
from gnf.types import TavalidatorcertAlgoTransfer_Maker
from gnf.types import TerminalassetCertifyHack_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatA_Maker]:
    return [
        BaseGNodeGt_Maker,
        BasegnodeCtnCreate_Maker,
        BasegnodeMarketmakerCreate_Maker,
        BasegnodeOtherCreate_Maker,
        BasegnodeTerminalassetCreate_Maker,
        BasegnodesBroadcast_Maker,
        BasegnodesGet_Maker,
        DebugTcReinitializeTime_Maker,
        DiscoverycertAlgoCreate_Maker,
        DiscoverycertAlgoTransfer_Maker,
        GwCertId_Maker,
        HeartbeatA_Maker,
        InitialTadeedAlgoCreate_Maker,
        InitialTadeedAlgoOptin_Maker,
        InitialTadeedAlgoTransfer_Maker,
        NewTadeedAlgoOptin_Maker,
        NewTadeedSend_Maker,
        OldTadeedAlgoReturn_Maker,
        PauseTime_Maker,
        ResumeTime_Maker,
        SlaEnter_Maker,
        TadeedSpecsHack_Maker,
        TatradingrightsAlgoCreate_Maker,
        TavalidatorcertAlgoCreate_Maker,
        TavalidatorcertAlgoTransfer_Maker,
        TerminalassetCertifyHack_Maker,
    ]


for maker in type_makers():
    TypeMakerByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "base.g.node.gt": "002",
        "basegnode.ctn.create": "000",
        "basegnode.marketmaker.create": "000",
        "basegnode.other.create": "000",
        "basegnode.terminalasset.create": "000",
        "basegnodes.broadcast": "000",
        "basegnodes.get": "000",
        "debug.tc.reinitialize.time": "000",
        "discoverycert.algo.create": "000",
        "discoverycert.algo.transfer": "000",
        "gw.cert.id": "000",
        "heartbeat.a": "100",
        "initial.tadeed.algo.create": "000",
        "initial.tadeed.algo.optin": "002",
        "initial.tadeed.algo.transfer": "000",
        "new.tadeed.algo.optin": "000",
        "new.tadeed.send": "000",
        "old.tadeed.algo.return": "000",
        "pause.time": "000",
        "resume.time": "000",
        "sla.enter": "000",
        "tadeed.specs.hack": "000",
        "tatradingrights.algo.create": "000",
        "tavalidatorcert.algo.create": "000",
        "tavalidatorcert.algo.transfer": "000",
        "terminalasset.certify.hack": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "base.g.node.gt.002": "Pending",
        "basegnode.ctn.create.000": "Pending",
        "basegnode.marketmaker.create.000": "Pending",
        "basegnode.other.create.000": "Pending",
        "basegnode.terminalasset.create.000": "Pending",
        "basegnodes.broadcast.000": "Pending",
        "basegnodes.get.000": "Pending",
        "debug.tc.reinitialize.time.000": "Pending",
        "discoverycert.algo.create.000": "Pending",
        "discoverycert.algo.transfer.000": "Pending",
        "gw.cert.id.000": "Pending",
        "heartbeat.a.100": "Pending",
        "initial.tadeed.algo.create.000": "Pending",
        "initial.tadeed.algo.optin.002": "Pending",
        "initial.tadeed.algo.transfer.000": "Pending",
        "new.tadeed.algo.optin.000": "Pending",
        "new.tadeed.send.000": "Pending",
        "old.tadeed.algo.return.000": "Pending",
        "pause.time.000": "Pending",
        "resume.time.000": "Pending",
        "sla.enter.000": "Pending",
        "tadeed.specs.hack.000": "Pending",
        "tatradingrights.algo.create.000": "Pending",
        "tavalidatorcert.algo.create.000": "Active",
        "tavalidatorcert.algo.transfer.000": "Active",
        "terminalasset.certify.hack.000": "Pending",
    }

    return v
