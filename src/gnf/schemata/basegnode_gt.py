"""basegnode.gt.020 type"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.data_classes import BaseGNode
from gnf.errors import SchemaError
from gnf.message import as_enum
from gnf.property_format import predicate_validator


class CoreGNodeRole100SchemaEnum:
    enum_name: str = "core.g.node.role.100"
    symbols: List[str] = [
        "00000000",
        "0f8872f7",
        "9521af06",
        "d9823442",
        "86f21dd2",
        "4502e355",
        "d67e564e",
    ]

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class CoreGNodeRole100(StrEnum):
    Other = auto()
    TerminalAsset = auto()
    AtomicMeteringNode = auto()
    AtomicTNode = auto()
    MarketMaker = auto()
    ConductorTopologyNode = auto()
    InterconnectionComponent = auto()

    @classmethod
    def default(cls) -> "CoreGNodeRole100":
        return cls.Other

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class CoreGNodeRoleMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not CoreGNodeRole100SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to CoreGNodeRole100 symbols")
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, core_g_node_role):
        if not isinstance(core_g_node_role, CoreGNodeRole100):
            raise SchemaError(f"{core_g_node_role} must be of type {CoreGNodeRole100}")
        return cls.local_to_type_dict[core_g_node_role]

    type_to_local_dict: Dict[str, CoreGNodeRole100] = {
        "00000000": CoreGNodeRole100.Other,
        "0f8872f7": CoreGNodeRole100.TerminalAsset,
        "9521af06": CoreGNodeRole100.AtomicMeteringNode,
        "d9823442": CoreGNodeRole100.AtomicTNode,
        "86f21dd2": CoreGNodeRole100.MarketMaker,
        "4502e355": CoreGNodeRole100.ConductorTopologyNode,
        "d67e564e": CoreGNodeRole100.InterconnectionComponent,
    }

    local_to_type_dict: Dict[CoreGNodeRole100, str] = {
        CoreGNodeRole100.Other: "00000000",
        CoreGNodeRole100.TerminalAsset: "0f8872f7",
        CoreGNodeRole100.AtomicMeteringNode: "9521af06",
        CoreGNodeRole100.AtomicTNode: "d9823442",
        CoreGNodeRole100.MarketMaker: "86f21dd2",
        CoreGNodeRole100.ConductorTopologyNode: "4502e355",
        CoreGNodeRole100.InterconnectionComponent: "d67e564e",
    }


class GNodeStatus100SchemaEnum:
    enum_name: str = "g.node.status.100"
    symbols: List[str] = [
        "00000000",
        "a2cfc2f7",
        "153d3475",
        "839b38db",
        "f5831e1d",
    ]

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class GNodeStatus100(StrEnum):
    Unknown = auto()
    Active = auto()
    Pending = auto()
    PermanentlyDeactivated = auto()
    Suspended = auto()

    @classmethod
    def default(cls) -> "GNodeStatus100":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class GNodeStatusMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not GNodeStatus100SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to GNodeStatus100 symbols")
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, g_node_status):
        if not isinstance(g_node_status, GNodeStatus100):
            raise SchemaError(f"{g_node_status} must be of type {GNodeStatus100}")
        return cls.local_to_type_dict[g_node_status]

    type_to_local_dict: Dict[str, GNodeStatus100] = {
        "00000000": GNodeStatus100.Unknown,
        "a2cfc2f7": GNodeStatus100.Active,
        "153d3475": GNodeStatus100.Pending,
        "839b38db": GNodeStatus100.PermanentlyDeactivated,
        "f5831e1d": GNodeStatus100.Suspended,
    }

    local_to_type_dict: Dict[GNodeStatus100, str] = {
        GNodeStatus100.Unknown: "00000000",
        GNodeStatus100.Active: "a2cfc2f7",
        GNodeStatus100.Pending: "153d3475",
        GNodeStatus100.PermanentlyDeactivated: "839b38db",
        GNodeStatus100.Suspended: "f5831e1d",
    }


class BasegnodeGt(BaseModel):
    Status: GNodeStatus100  #
    GNodeRegistryAddr: str  #
    Role: CoreGNodeRole100  #
    Alias: str  #
    GNodeId: int  #
    PrevAlias: Optional[str] = None
    TradingRightsNftId: Optional[int] = None
    OwnershipDeedValidatorAddr: Optional[str] = None
    OwnershipDeedNftId: Optional[int] = None
    OwnerAddr: Optional[str] = None
    DaemonAddr: Optional[str] = None
    GpsPointId: Optional[str] = None
    TypeName: Literal["basegnode.gt"] = "basegnode.gt"

    @validator("Status", pre=True)
    def _validator_status(cls, v: Any) -> GNodeStatus100:
        return as_enum(v, GNodeStatus100, GNodeStatus100.Unknown)

    _validator_g_node_registry_addr = predicate_validator(
        "GNodeRegistryAddr", property_format.is_algo_address_string_format
    )

    @validator("Role", pre=True)
    def _validator_role(cls, v: Any) -> CoreGNodeRole100:
        return as_enum(v, CoreGNodeRole100, CoreGNodeRole100.Other)

    @validator("PrevAlias")
    def _validator_prev_alias(cls, v: Any) -> Optional[str]:
        if not property_format.is_lrd_alias_format(v):
            raise ValueError(f"PrevAlias {v} must have LrdAliasFormat")

    @validator("OwnershipDeedValidatorAddr")
    def _validator_ownership_deed_validator_addr(cls, v: Any) -> Optional[str]:
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(
                f"OwnershipDeedValidatorAddr {v} must have AlgoAddressStringFormat"
            )

    _validator_alias = predicate_validator("Alias", property_format.is_lrd_alias_format)

    _validator_g_node_id = predicate_validator(
        "GNodeId", property_format.is_uuid_canonical_textual
    )

    @validator("OwnershipDeedNftId")
    def _validator_ownership_deed_nft_id(cls, v: Any) -> Optional[int]:
        if not property_format.is_positive_integer(v):
            raise ValueError(f"OwnershipDeedNftId {v} must have PositiveInteger")

    @validator("OwnerAddr")
    def _validator_owner_addr(cls, v: Any) -> Optional[str]:
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(f"OwnerAddr {v} must have AlgoAddressStringFormat")

    @validator("DaemonAddr")
    def _validator_daemon_addr(cls, v: Any) -> Optional[str]:
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(f"DaemonAddr {v} must have AlgoAddressStringFormat")

    @validator("GpsPointId")
    def _validator_gps_point_id(cls, v: Any) -> Optional[str]:
        if not property_format.is_uuid_canonical_textual(v):
            raise ValueError(f"GpsPointId {v} must have UuidCanonicalTextual")

    def as_dict(self) -> Dict:
        d = self.dict()
        del d["Status"]
        d["StatusGtEnumSymbol"] = GNodeStatusMap.local_to_type(self.Status)
        del d["Role"]
        d["RoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_type(self.Role)
        if d["PrevAlias"] is None:
            del d["PrevAlias"]
        if d["TradingRightsNftId"] is None:
            del d["TradingRightsNftId"]
        if d["OwnershipDeedValidatorAddr"] is None:
            del d["OwnershipDeedValidatorAddr"]
        if d["OwnershipDeedNftId"] is None:
            del d["OwnershipDeedNftId"]
        if d["OwnerAddr"] is None:
            del d["OwnerAddr"]
        if d["DaemonAddr"] is None:
            del d["DaemonAddr"]
        if d["GpsPointId"] is None:
            del d["GpsPointId"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeGt_Maker:
    type_name = "basegnode.gt"

    def __init__(
        self,
        status: GNodeStatus100,
        g_node_registry_addr: str,
        role: CoreGNodeRole100,
        alias: str,
        g_node_id: int,
        prev_alias: Optional[str],
        trading_rights_nft_id: Optional[int],
        ownership_deed_validator_addr: Optional[str],
        ownership_deed_nft_id: Optional[int],
        owner_addr: Optional[str],
        daemon_addr: Optional[str],
        gps_point_id: Optional[str],
    ):

        self.tuple = BasegnodeGt(
            Status=status,
            GNodeRegistryAddr=g_node_registry_addr,
            Role=role,
            PrevAlias=prev_alias,
            TradingRightsNftId=trading_rights_nft_id,
            OwnershipDeedValidatorAddr=ownership_deed_validator_addr,
            Alias=alias,
            GNodeId=g_node_id,
            OwnershipDeedNftId=ownership_deed_nft_id,
            OwnerAddr=owner_addr,
            DaemonAddr=daemon_addr,
            GpsPointId=gps_point_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeGt) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeGt:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> BasegnodeGt:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")
        if "StatusGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StatusGtEnumSymbol")
        if d2["StatusGtEnumSymbol"] in GNodeStatus100SchemaEnum.symbols:
            d2["Status"] = GNodeStatusMap.type_to_local(d2["StatusGtEnumSymbol"])
        else:
            d2["Status"] = GNodeStatus100.Unknown
        if "RoleGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RoleGtEnumSymbol")
        if d2["RoleGtEnumSymbol"] in CoreGNodeRole100SchemaEnum.symbols:
            d2["Role"] = CoreGNodeRoleMap.type_to_local(d2["RoleGtEnumSymbol"])
        else:
            d2["Role"] = CoreGNodeRole100.Other
        if "PrevAlias" not in d2.keys():
            d2["PrevAlias"] = None
        if "TradingRightsNftId" not in d2.keys():
            d2["TradingRightsNftId"] = None
        if "OwnershipDeedValidatorAddr" not in d2.keys():
            d2["OwnershipDeedValidatorAddr"] = None
        if "OwnershipDeedNftId" not in d2.keys():
            d2["OwnershipDeedNftId"] = None
        if "OwnerAddr" not in d2.keys():
            d2["OwnerAddr"] = None
        if "DaemonAddr" not in d2.keys():
            d2["DaemonAddr"] = None
        if "GpsPointId" not in d2.keys():
            d2["GpsPointId"] = None

        return BasegnodeGt(
            TypeName=d2["TypeName"],
            Status=d2["Status"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            Role=d2["Role"],
            PrevAlias=d2["PrevAlias"],
            TradingRightsNftId=d2["TradingRightsNftId"],
            OwnershipDeedValidatorAddr=d2["OwnershipDeedValidatorAddr"],
            Alias=d2["Alias"],
            GNodeId=d2["GNodeId"],
            OwnershipDeedNftId=d2["OwnershipDeedNftId"],
            OwnerAddr=d2["OwnerAddr"],
            DaemonAddr=d2["DaemonAddr"],
            GpsPointId=d2["GpsPointId"],
        )

    @classmethod
    def tuple_to_dc(cls, t: BasegnodeGt) -> BaseGNode:
        s = {
            "status": t.Status,
            "g_node_registry_addr": t.GNodeRegistryAddr,
            "role": t.Role,
            "prev_alias": t.PrevAlias,
            "trading_rights_nft_id": t.TradingRightsNftId,
            "ownership_deed_validator_addr": t.OwnershipDeedValidatorAddr,
            "alias": t.Alias,
            "g_node_id": t.GNodeId,
            "ownership_deed_nft_id": t.OwnershipDeedNftId,
            "owner_addr": t.OwnerAddr,
            "daemon_addr": t.DaemonAddr,
            "gps_point_id": t.GpsPointId,
        }
        if s["base_g_node_id"] in BaseGNode.by_id.keys():
            dc = BaseGNode.by_id[s["base_g_node_id"]]
        else:
            dc = BaseGNode(**s)
        return dc

    @classmethod
    def dc_to_tuple(cls, dc: BaseGNode) -> BasegnodeGt:
        if dc is None:
            return None
        t = BasegnodeGt_Maker(
            status=dc.status,
            g_node_registry_addr=dc.g_node_registry_addr,
            role=dc.role,
            prev_alias=dc.prev_alias,
            trading_rights_nft_id=dc.trading_rights_nft_id,
            ownership_deed_validator_addr=dc.ownership_deed_validator_addr,
            alias=dc.alias,
            g_node_id=dc.g_node_id,
            ownership_deed_nft_id=dc.ownership_deed_nft_id,
            owner_addr=dc.owner_addr,
            daemon_addr=dc.daemon_addr,
            gps_point_id=dc.gps_point_id,
        ).tuple
        return t

    @classmethod
    def type_to_dc(cls, t: str) -> BaseGNode:
        return cls.tuple_to_dc(cls.type_to_tuple(t))

    @classmethod
    def dc_to_type(cls, dc: BaseGNode) -> str:
        return cls.dc_to_tuple(dc).as_type()

    @classmethod
    def dict_to_dc(cls, d: dict) -> BaseGNode:
        return cls.tuple_to_dc(cls.dict_to_tuple(d))
