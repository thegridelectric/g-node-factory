"""Base for create.tadeed.algo.010 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class CreateTadeedAlgoBase(NamedTuple):
    ValidatorAddr: str  #
    HalfSignedDeedCreationMtx: str  #
    TypeName: str = "create.tadeed.algo.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.HalfSignedDeedCreationMtx, str):
            errors.append(
                f"HalfSignedDeedCreationMtx {self.HalfSignedDeedCreationMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedDeedCreationMtx
            )
        except SchemaError as e:
            errors.append(
                f"HalfSignedDeedCreationMtx {self.HalfSignedDeedCreationMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if self.TypeName != "create.tadeed.algo.010":
            errors.append(
                f"Type requires TypeName of create.tadeed.algo.010, not {self.TypeName}."
            )

        return errors
