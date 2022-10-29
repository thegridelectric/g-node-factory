"""Base for basegnode.020 """


import json
from typing import List
from typing import NamedTuple
from typing import Optional

import property_format
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap
from errors import SchemaError


class BasegnodeBase(NamedTuple):
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
