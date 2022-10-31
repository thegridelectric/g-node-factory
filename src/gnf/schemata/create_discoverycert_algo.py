"""create.discoverycert.algo.001 type"""

import json
from enum import auto
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional

from fastapi_utils.enums import StrEnum

import gnf.property_format as property_format
from gnf.errors import SchemaError


class CoreGNodeRole100SchemaEnum:
    enum_name: str = "core.g.node.role.100"
    symbols: List[str] = [
        "4502e355",
        "d9823442",
        "0f8872f7",
        "d67e564e",
        "00000000",
        "86f21dd2",
        "9521af06",
    ]

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class CoreGNodeRole100(StrEnum):
    ConductorTopologyNode = auto()
    AtomicTNode = auto()
    TerminalAsset = auto()
    InterconnectionComponent = auto()
    Other = auto()
    MarketMaker = auto()
    AtomicMeteringNode = auto()

    @classmethod
    def values(cls):
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
        "4502e355": CoreGNodeRole100.ConductorTopologyNode,
        "d9823442": CoreGNodeRole100.AtomicTNode,
        "0f8872f7": CoreGNodeRole100.TerminalAsset,
        "d67e564e": CoreGNodeRole100.InterconnectionComponent,
        "00000000": CoreGNodeRole100.Other,
        "86f21dd2": CoreGNodeRole100.MarketMaker,
        "9521af06": CoreGNodeRole100.AtomicMeteringNode,
    }

    local_to_type_dict: Dict[CoreGNodeRole100, str] = {
        CoreGNodeRole100.ConductorTopologyNode: "4502e355",
        CoreGNodeRole100.AtomicTNode: "d9823442",
        CoreGNodeRole100.TerminalAsset: "0f8872f7",
        CoreGNodeRole100.InterconnectionComponent: "d67e564e",
        CoreGNodeRole100.Other: "00000000",
        CoreGNodeRole100.MarketMaker: "86f21dd2",
        CoreGNodeRole100.AtomicMeteringNode: "9521af06",
    }


class CreateDiscoverycertAlgo(NamedTuple):
    OldChildAliasList: List[str]
    GNodeAlias: str  #
    CoreGNodeRole: CoreGNodeRole100  #
    DiscovererAddr: str  #
    SupportingMaterialHash: str  #
    MicroLon: Optional[int] = None
    MicroLat: Optional[int] = None
    TypeName: str = "create.discoverycert.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        del d["CoreGNodeRole"]
        d["CoreGNodeRoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_type(
            self.CoreGNodeRole
        )
        if d["MicroLon"] is None:
            del d["MicroLon"]
        if d["MicroLat"] is None:
            del d["MicroLat"]
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.OldChildAliasList, list):
            errors.append(
                f"OldChildAliasList {self.OldChildAliasList} must have type list."
            )
        else:
            for elt in self.OldChildAliasList:
                if not isinstance(elt, str):
                    errors.append(f"elt {elt} of OldChildAliasList must have type str.")
                try:
                    property_format.check_is_lrd_alias_format(elt)
                except SchemaError as e:
                    errors.append(
                        f"elt {elt} of OldChildAliasList must have format LrdAliasFormat; {e}"
                    )
        if not isinstance(self.GNodeAlias, str):
            errors.append(f"GNodeAlias {self.GNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.GNodeAlias)
        except SchemaError as e:
            errors.append(
                f"GNodeAlias {self.GNodeAlias}" " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.CoreGNodeRole, CoreGNodeRole100):
            errors.append(
                f"CoreGNodeRole {self.CoreGNodeRole} must have type {CoreGNodeRole100}."
            )
        if not isinstance(self.DiscovererAddr, str):
            errors.append(f"DiscovererAddr {self.DiscovererAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.DiscovererAddr)
        except SchemaError as e:
            errors.append(
                f"DiscovererAddr {self.DiscovererAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.MicroLon:
            if not isinstance(self.MicroLon, int):
                errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if not isinstance(self.SupportingMaterialHash, str):
            errors.append(
                f"SupportingMaterialHash {self.SupportingMaterialHash} must have type str."
            )
        if self.MicroLat:
            if not isinstance(self.MicroLat, int):
                errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if self.TypeName != "create.discoverycert.algo.001":
            errors.append(
                f"Type requires TypeName of create.discoverycert.algo.001, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.discoverycert.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateDiscoverycertAlgo"

    def hand_coded_errors(self):
        return []


class CreateDiscoverycertAlgo_Maker:
    type_name = "create.discoverycert.algo.001"

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

        gw_tuple = CreateDiscoverycertAlgo(
            OldChildAliasList=old_child_alias_list,
            GNodeAlias=g_node_alias,
            CoreGNodeRole=core_g_node_role,
            DiscovererAddr=discoverer_addr,
            MicroLon=micro_lon,
            SupportingMaterialHash=supporting_material_hash,
            MicroLat=micro_lat,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateDiscoverycertAlgo) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "OldChildAliasList" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing OldChildAliasList")
        if "GNodeAlias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeAlias")
        if "CoreGNodeRoleGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing CoreGNodeRoleGtEnumSymbol")
        new_d["CoreGNodeRole"] = CoreGNodeRoleMap.type_to_local(
            new_d["CoreGNodeRoleGtEnumSymbol"]
        )
        if "DiscovererAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DiscovererAddr")
        if "MicroLon" not in new_d.keys():
            new_d["MicroLon"] = None
        if "SupportingMaterialHash" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing SupportingMaterialHash")
        if "MicroLat" not in new_d.keys():
            new_d["MicroLat"] = None

        gw_tuple = CreateDiscoverycertAlgo(
            TypeName=new_d["TypeName"],
            OldChildAliasList=new_d["OldChildAliasList"],
            GNodeAlias=new_d["GNodeAlias"],
            CoreGNodeRole=new_d["CoreGNodeRole"],
            DiscovererAddr=new_d["DiscovererAddr"],
            MicroLon=new_d["MicroLon"],
            SupportingMaterialHash=new_d["SupportingMaterialHash"],
            MicroLat=new_d["MicroLat"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
