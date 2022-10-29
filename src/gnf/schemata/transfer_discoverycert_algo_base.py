"""Base for transfer.discoverycert.algo.001 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class TransferDiscoverycertAlgoBase(NamedTuple):
    GNodeAlias: str  #
    DiscovererAddr: str  #
    TypeName: str = "transfer.discoverycert.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
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
        if self.TypeName != "transfer.discoverycert.algo.001":
            errors.append(
                f"Type requires TypeName of transfer.discoverycert.algo.001, not {self.TypeName}."
            )

        return errors
