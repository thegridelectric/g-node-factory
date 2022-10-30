"""basegnode.gt.020 type"""

import json
from enum import auto
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional

from fastapi_utils.enums import StrEnum

import gnf.property_format as property_format
from gnf.data_classes import BaseGNode
from gnf.errors import SchemaError


class CoreGNodeRole100SchemaEnum:
    enum_name: str = "core.g.node.role.100"
    symbols: List[str] = [
        "4502e355",
        "d9823442",
        "0f8872f7",
        "d67e564e",
        "6b58d301",
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
        "6b58d301": CoreGNodeRole100.Other,
        "86f21dd2": CoreGNodeRole100.MarketMaker,
        "9521af06": CoreGNodeRole100.AtomicMeteringNode,
    }

    local_to_type_dict: Dict[CoreGNodeRole100, str] = {
        CoreGNodeRole100.ConductorTopologyNode: "4502e355",
        CoreGNodeRole100.AtomicTNode: "d9823442",
        CoreGNodeRole100.TerminalAsset: "0f8872f7",
        CoreGNodeRole100.InterconnectionComponent: "d67e564e",
        CoreGNodeRole100.Other: "6b58d301",
        CoreGNodeRole100.MarketMaker: "86f21dd2",
        CoreGNodeRole100.AtomicMeteringNode: "9521af06",
    }


class GNodeStatus100SchemaEnum:
    enum_name: str = "g.node.status.100"
    symbols: List[str] = [
        "839b38db",
        "153d3475",
        "8d92bebe",
        "f5831e1d",
    ]

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class GNodeStatus100(StrEnum):
    PermanentlyDeactivated = auto()
    Pending = auto()
    Active = auto()
    Suspended = auto()

    @classmethod
    def values(cls):
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
        "839b38db": GNodeStatus100.PermanentlyDeactivated,
        "153d3475": GNodeStatus100.Pending,
        "8d92bebe": GNodeStatus100.Active,
        "f5831e1d": GNodeStatus100.Suspended,
    }

    local_to_type_dict: Dict[GNodeStatus100, str] = {
        GNodeStatus100.PermanentlyDeactivated: "839b38db",
        GNodeStatus100.Pending: "153d3475",
        GNodeStatus100.Active: "8d92bebe",
        GNodeStatus100.Suspended: "f5831e1d",
    }


class BasegnodeGt(NamedTuple):
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
    TypeName: str = "basegnode.gt.020"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
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

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.Status, GNodeStatus100):
            errors.append(f"Status {self.Status} must have type {GNodeStatus100}.")
        if not isinstance(self.GNodeRegistryAddr, str):
            errors.append(
                f"GNodeRegistryAddr {self.GNodeRegistryAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.GNodeRegistryAddr)
        except SchemaError as e:
            errors.append(
                f"GNodeRegistryAddr {self.GNodeRegistryAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.Role, CoreGNodeRole100):
            errors.append(f"Role {self.Role} must have type {CoreGNodeRole100}.")
        if self.PrevAlias:
            if not isinstance(self.PrevAlias, str):
                errors.append(f"PrevAlias {self.PrevAlias} must have type str.")
            try:
                property_format.check_is_lrd_alias_format(self.PrevAlias)
            except SchemaError as e:
                errors.append(
                    f"PrevAlias {self.PrevAlias}"
                    " must have format LrdAliasFormat: {e}"
                )
        if self.TradingRightsNftId:
            if not isinstance(self.TradingRightsNftId, int):
                errors.append(
                    f"TradingRightsNftId {self.TradingRightsNftId} must have type int."
                )
        if self.OwnershipDeedValidatorAddr:
            if not isinstance(self.OwnershipDeedValidatorAddr, str):
                errors.append(
                    f"OwnershipDeedValidatorAddr {self.OwnershipDeedValidatorAddr} must have type str."
                )
            try:
                property_format.check_is_algo_address_string_format(
                    self.OwnershipDeedValidatorAddr
                )
            except SchemaError as e:
                errors.append(
                    f"OwnershipDeedValidatorAddr {self.OwnershipDeedValidatorAddr}"
                    " must have format AlgoAddressStringFormat: {e}"
                )
        if not isinstance(self.Alias, str):
            errors.append(f"Alias {self.Alias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.Alias)
        except SchemaError as e:
            errors.append(f"Alias {self.Alias}" " must have format LrdAliasFormat: {e}")
        if not isinstance(self.GNodeId, int):
            errors.append(f"GNodeId {self.GNodeId} must have type int.")
        try:
            property_format.check_is_uuid_canonical_textual(self.GNodeId)
        except SchemaError as e:
            errors.append(
                f"GNodeId {self.GNodeId}" " must have format UuidCanonicalTextual: {e}"
            )
        if self.OwnershipDeedNftId:
            if not isinstance(self.OwnershipDeedNftId, int):
                errors.append(
                    f"OwnershipDeedNftId {self.OwnershipDeedNftId} must have type int."
                )
            try:
                property_format.check_is_positive_integer(self.OwnershipDeedNftId)
            except SchemaError as e:
                errors.append(
                    f"OwnershipDeedNftId {self.OwnershipDeedNftId}"
                    " must have format PositiveInteger: {e}"
                )
        if self.OwnerAddr:
            if not isinstance(self.OwnerAddr, str):
                errors.append(f"OwnerAddr {self.OwnerAddr} must have type str.")
            try:
                property_format.check_is_algo_address_string_format(self.OwnerAddr)
            except SchemaError as e:
                errors.append(
                    f"OwnerAddr {self.OwnerAddr}"
                    " must have format AlgoAddressStringFormat: {e}"
                )
        if self.DaemonAddr:
            if not isinstance(self.DaemonAddr, str):
                errors.append(f"DaemonAddr {self.DaemonAddr} must have type str.")
            try:
                property_format.check_is_algo_address_string_format(self.DaemonAddr)
            except SchemaError as e:
                errors.append(
                    f"DaemonAddr {self.DaemonAddr}"
                    " must have format AlgoAddressStringFormat: {e}"
                )
        if self.GpsPointId:
            if not isinstance(self.GpsPointId, str):
                errors.append(f"GpsPointId {self.GpsPointId} must have type str.")
            try:
                property_format.check_is_uuid_canonical_textual(self.GpsPointId)
            except SchemaError as e:
                errors.append(
                    f"GpsPointId {self.GpsPointId}"
                    " must have format UuidCanonicalTextual: {e}"
                )
        if self.TypeName != "basegnode.gt.020":
            errors.append(
                f"Type requires TypeName of basegnode.gt.020, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making basegnode.gt.020 for {self}: {errors}")

    def __repr__(self):
        return "BasegnodeGt"

    def hand_coded_errors(self):
        return []


class BasegnodeGt_Maker:
    type_name = "basegnode.gt.020"

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

        gw_tuple = BasegnodeGt(
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
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeGt) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "StatusGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing StatusGtEnumSymbol")
        new_d["Status"] = GNodeStatusMap.type_to_local(new_d["StatusGtEnumSymbol"])
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "RoleGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing RoleGtEnumSymbol")
        new_d["Role"] = CoreGNodeRoleMap.type_to_local(new_d["RoleGtEnumSymbol"])
        if "PrevAlias" not in new_d.keys():
            new_d["PrevAlias"] = None
        if "TradingRightsNftId" not in new_d.keys():
            new_d["TradingRightsNftId"] = None
        if "OwnershipDeedValidatorAddr" not in new_d.keys():
            new_d["OwnershipDeedValidatorAddr"] = None
        if "Alias" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Alias")
        if "GNodeId" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeId")
        if "OwnershipDeedNftId" not in new_d.keys():
            new_d["OwnershipDeedNftId"] = None
        if "OwnerAddr" not in new_d.keys():
            new_d["OwnerAddr"] = None
        if "DaemonAddr" not in new_d.keys():
            new_d["DaemonAddr"] = None
        if "GpsPointId" not in new_d.keys():
            new_d["GpsPointId"] = None

        gw_tuple = BasegnodeGt(
            TypeName=new_d["TypeName"],
            Status=new_d["Status"],
            GNodeRegistryAddr=new_d["GNodeRegistryAddr"],
            Role=new_d["Role"],
            PrevAlias=new_d["PrevAlias"],
            TradingRightsNftId=new_d["TradingRightsNftId"],
            OwnershipDeedValidatorAddr=new_d["OwnershipDeedValidatorAddr"],
            Alias=new_d["Alias"],
            GNodeId=new_d["GNodeId"],
            OwnershipDeedNftId=new_d["OwnershipDeedNftId"],
            OwnerAddr=new_d["OwnerAddr"],
            DaemonAddr=new_d["DaemonAddr"],
            GpsPointId=new_d["GpsPointId"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple

    @classmethod
    def tuple_to_dc(cls, t: BasegnodeGt) -> BaseGNode:
        s = {
            "g_node_registry_addr": t.GNodeRegistryAddr,
            "prev_alias": t.PrevAlias,
            "trading_rights_nft_id": t.TradingRightsNftId,
            "ownership_deed_validator_addr": t.OwnershipDeedValidatorAddr,
            "alias": t.Alias,
            "g_node_id": t.GNodeId,
            "ownership_deed_nft_id": t.OwnershipDeedNftId,
            "owner_addr": t.OwnerAddr,
            "daemon_addr": t.DaemonAddr,
            "gps_point_id": t.GpsPointId,
            "status_gt_enum_symbol": GNodeStatusMap.local_to_type(t.Status),
            "role_gt_enum_symbol": CoreGNodeRoleMap.local_to_type(t.Role),
            #
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
        t = BasegnodeGt(
            Status=dc.status,
            GNodeRegistryAddr=dc.g_node_registry_addr,
            Role=dc.role,
            PrevAlias=dc.prev_alias,
            TradingRightsNftId=dc.trading_rights_nft_id,
            OwnershipDeedValidatorAddr=dc.ownership_deed_validator_addr,
            Alias=dc.alias,
            GNodeId=dc.g_node_id,
            OwnershipDeedNftId=dc.ownership_deed_nft_id,
            OwnerAddr=dc.owner_addr,
            DaemonAddr=dc.daemon_addr,
            GpsPointId=dc.gps_point_id,
            #
        )
        t.check_for_errors()
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
