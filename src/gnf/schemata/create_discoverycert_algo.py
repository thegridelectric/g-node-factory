"""create.discoverycert.algo.001 type"""
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


class CreateDiscoverycertAlgo(BaseModel):
    OldChildAliasList: List[str]
    GNodeAlias: str  #
    CoreGNodeRole: CoreGNodeRole100  #
    DiscovererAddr: str  #
    SupportingMaterialHash: str  #
    MicroLon: Optional[int] = None
    MicroLat: Optional[int] = None
    TypeName: Literal["create.discoverycert.algo"] = "create.discoverycert.algo"

    @validator("OldChildAliasList")
    def _validator_old_child_alias_list(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_lrd_alias_format(elt):
                raise ValueError(
                    f"failure of predicate is_lrd_alias_format() on elt {elt} of OldChildAliasList"
                )
        return v

    _validator_g_node_alias = predicate_validator(
        "GNodeAlias", property_format.is_lrd_alias_format
    )

    @validator("CoreGNodeRole", pre=True)
    def _validator_core_g_node_role(cls, v: Any) -> CoreGNodeRole100:
        return as_enum(v, CoreGNodeRole100, CoreGNodeRole100.Other)

    _validator_discoverer_addr = predicate_validator(
        "DiscovererAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        del d["CoreGNodeRole"]
        d["CoreGNodeRoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_type(
            self.CoreGNodeRole
        )
        if d["MicroLon"] is None:
            del d["MicroLon"]
        if d["MicroLat"] is None:
            del d["MicroLat"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateDiscoverycertAlgo_Maker:
    type_name = "create.discoverycert.algo"

    def __init__(
        self,
        old_child_alias_list: List[str],
        g_node_alias: str,
        core_g_node_role: CoreGNodeRole100,
        discoverer_addr: str,
        supporting_material_hash: str,
        micro_lon: Optional[int],
        micro_lat: Optional[int],
    ):

        self.tuple = CreateDiscoverycertAlgo(
            OldChildAliasList=old_child_alias_list,
            GNodeAlias=g_node_alias,
            CoreGNodeRole=core_g_node_role,
            DiscovererAddr=discoverer_addr,
            MicroLon=micro_lon,
            SupportingMaterialHash=supporting_material_hash,
            MicroLat=micro_lat,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateDiscoverycertAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateDiscoverycertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateDiscoverycertAlgo:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")
        if "CoreGNodeRoleGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CoreGNodeRoleGtEnumSymbol")
        if d2["CoreGNodeRoleGtEnumSymbol"] in CoreGNodeRole100SchemaEnum.symbols:
            d2["CoreGNodeRole"] = CoreGNodeRoleMap.type_to_local(
                d2["CoreGNodeRoleGtEnumSymbol"]
            )
        else:
            d2["CoreGNodeRole"] = CoreGNodeRole100.Other
        if "MicroLon" not in d2.keys():
            d2["MicroLon"] = None
        if "MicroLat" not in d2.keys():
            d2["MicroLat"] = None

        return CreateDiscoverycertAlgo(
            TypeName=d2["TypeName"],
            OldChildAliasList=d2["OldChildAliasList"],
            GNodeAlias=d2["GNodeAlias"],
            CoreGNodeRole=d2["CoreGNodeRole"],
            DiscovererAddr=d2["DiscovererAddr"],
            MicroLon=d2["MicroLon"],
            SupportingMaterialHash=d2["SupportingMaterialHash"],
            MicroLat=d2["MicroLat"],
        )
