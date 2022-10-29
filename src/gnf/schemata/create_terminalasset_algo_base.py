"""Base for create.terminalasset.algo.010 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class CreateTerminalassetAlgoBase(NamedTuple):
    TaGNodeAlias: str  #
    MicroLon: int  #
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    MicroLat: int  #
    GNodeRegistryAddr: str  #
    FromGNodeInstanceId: str  #
    FromGNodeAlias: str  #
    TypeName: str = "create.terminalasset.algo.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.TaGNodeAlias, str):
            errors.append(f"TaGNodeAlias {self.TaGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.TaGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"TaGNodeAlias {self.TaGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except SchemaError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
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
        if not isinstance(self.FromGNodeAlias, str):
            errors.append(f"FromGNodeAlias {self.FromGNodeAlias} must have type str.")
        try:
            property_format.check_is_lrd_alias_format(self.FromGNodeAlias)
        except SchemaError as e:
            errors.append(
                f"FromGNodeAlias {self.FromGNodeAlias}"
                " must have format LrdAliasFormat: {e}"
            )
        if self.TypeName != "create.terminalasset.algo.010":
            errors.append(
                f"Type requires TypeName of create.terminalasset.algo.010, not {self.TypeName}."
            )

        return errors
