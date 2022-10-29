"""Base for create.ctn.algo.001 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class CreateCtnAlgoBase(NamedTuple):
    ChildAliasList: List[str]
    FromGNodeAlias: str  #
    MicroLat: int  #
    MicroLon: int  #
    CtnGNodeAlias: str  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    TypeName: str = "create.ctn.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.ChildAliasList, list):
            errors.append(f"ChildAliasList {self.ChildAliasList} must have type list.")
        else:
            for elt in self.ChildAliasList:
                if not isinstance(elt, str):
                    errors.append(f"elt {elt} of ChildAliasList must have type str.")
                try:
                    property_format.check_is_lrd_alias_format(elt)
                except SchemaError as e:
                    errors.append(
                        f"elt {elt} of ChildAliasList must have format LrdAliasFormat; {e}"
                    )
        if not isinstance(self.FromGNodeAlias, str):
            errors.append(f"FromGNodeAlias {self.FromGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.FromGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"FromGNodeAlias {self.FromGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if not isinstance(self.CtnGNodeAlias, str):
            errors.append(f"CtnGNodeAlias {self.CtnGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.CtnGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"CtnGNodeAlias {self.CtnGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
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
        if not isinstance(self.FromGNodeInstanceId, str):
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId} must have type str."
            )
        try:
            property_format.check_is_uuid_canonical_textual(self.FromGNodeInstanceId)
        except SchemaError as e:
            errors.append(
                f"FromGNodeInstanceId {self.FromGNodeInstanceId}"
                " must have format UuidCanonicalTextual: {e}"
            )
        if self.TypeName != "create.ctn.algo.001":
            errors.append(
                f"Type requires TypeName of create.ctn.algo.001, not {self.TypeName}."
            )

        return errors
