"""basegnode.020 type"""

import json
from typing import NamedTuple
from typing import Optional

from data_classes.base_g_node import BaseGNode
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap

import gnf.property_format as property_format
from gnf.errors import SchemaError


class Basegnode(NamedTuple):
    Status: GNodeStatus  #
    GNodeRegistryAddr: str  #
    Role: CoreGNodeRole  #
    Alias: str  #
    GNodeId: int  #
    PrevAlias: Optional[str] = None
    TradingRightsNftId: Optional[int] = None
    OwnershipDeedValidatorAddr: Optional[str] = None
    OwnershipDeedNftId: Optional[int] = None
    OwnerAddr: Optional[str] = None
    DaemonAddr: Optional[str] = None
    GpsPointId: Optional[str] = None
    TypeName: str = "basegnode.020"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        del d["Status"]
        d["StatusGtEnumSymbol"] = GNodeStatusMap.local_to_gt(self.Status)
        del d["Role"]
        d["RoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_gt(self.Role)
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
        if not isinstance(self.Status, GNodeStatus):
            errors.append(f"Status {self.Status} must have type {GNodeStatus}.")
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
        if not isinstance(self.Role, CoreGNodeRole):
            errors.append(f"Role {self.Role} must have type {CoreGNodeRole}.")
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
        if self.TypeName != "basegnode.020":
            errors.append(
                f"Type requires TypeName of basegnode.020, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making basegnode.020 for {self}: {errors}")

    def __repr__(self):
        return "Basegnode"

    def hand_coded_errors(self):
        return []


class Basegnode_Maker:
    type_name = "basegnode.020"

    def __init__(
        self,
        status: GNodeStatus,
        g_node_registry_addr: str,
        role: CoreGNodeRole,
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

        gw_tuple = Basegnode(
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
    def tuple_to_type(cls, tuple: Basegnode) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> Basegnode:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> Basegnode:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "StatusGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing StatusGtEnumSymbol")
        new_d["Status"] = GNodeStatusMap.gt_to_local(new_d["StatusGtEnumSymbol"])
        if "GNodeRegistryAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing GNodeRegistryAddr")
        if "RoleGtEnumSymbol" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing RoleGtEnumSymbol")
        new_d["Role"] = CoreGNodeRoleMap.gt_to_local(new_d["RoleGtEnumSymbol"])
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

        gw_tuple = Basegnode(
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
    def tuple_to_dc(cls, t: Basegnode) -> BaseGNode:
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
            "status_gt_enum_symbol": GNodeStatusMap.local_to_gt(t.Status),
            "role_gt_enum_symbol": CoreGNodeRoleMap.local_to_gt(t.Role),
            #
        }
        if s["base_g_node_id"] in BaseGNode.by_id.keys():
            dc = BaseGNode.by_id[s["base_g_node_id"]]
        else:
            dc = BaseGNode(**s)
        return dc

    @classmethod
    def dc_to_tuple(cls, dc: BaseGNode) -> Basegnode:
        if dc is None:
            return None
        t = Basegnode(
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
