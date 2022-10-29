"""Base for create.tavalidatorcert.algo.010 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class CreateTavalidatorcertAlgoBase(NamedTuple):
    HalfSignedCertCreationMtx: str  #
    ValidatorAddr: str  #
    TypeName: str = "create.tavalidatorcert.algo.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.HalfSignedCertCreationMtx, str):
            errors.append(
                f"HalfSignedCertCreationMtx {self.HalfSignedCertCreationMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedCertCreationMtx
            )
        except SchemaError as e:
            errors.append(
                f"HalfSignedCertCreationMtx {self.HalfSignedCertCreationMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "create.tavalidatorcert.algo.010":
            errors.append(
                f"Type requires TypeName of create.tavalidatorcert.algo.010, not {self.TypeName}."
            )

        return errors
