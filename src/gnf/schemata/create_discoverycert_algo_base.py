"""Base for create.discoverycert.algo.001 """


import json
from typing import List
from typing import NamedTuple
from typing import Optional

import property_format
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from errors import SchemaError


class CreateDiscoverycertAlgoBase(NamedTuple):
    OldChildAliasList: List[str]
    GNodeAlias: str  #
    DiscovererAddr: str  #
    SupportingMaterialHash: str  #
    CoreGNodeRole: CoreGNodeRole  #
    MicroLon: Optional[int] = None
    MicroLat: Optional[int] = None
    TypeName: str = "create.discoverycert.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        if d["MicroLon"] is None:
            del d["MicroLon"]
        del d["CoreGNodeRole"]
        d["CoreGNodeRoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_gt(
            self.CoreGNodeRole
        )
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
        if not isinstance(self.CoreGNodeRole, CoreGNodeRole):
            errors.append(
                f"CoreGNodeRole {self.CoreGNodeRole} must have type {CoreGNodeRole}."
            )
        if self.MicroLat:
            if not isinstance(self.MicroLat, int):
                errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if self.TypeName != "create.discoverycert.algo.001":
            errors.append(
                f"Type requires TypeName of create.discoverycert.algo.001, not {self.TypeName}."
            )

        return errors
