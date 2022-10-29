"""Base for signandsubmit.mtx.algo.000 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class SignandsubmitMtxAlgoBase(NamedTuple):
    SignerAddress: str  #
    Mtx: str  #
    Addresses: List[str]
    Threshold: int  #
    TypeName: str = "signandsubmit.mtx.algo.000"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.SignerAddress, str):
            errors.append(f"SignerAddress {self.SignerAddress} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.SignerAddress)
        except SchemaError as e:
            errors.append(
                f"SignerAddress {self.SignerAddress}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.Mtx, str):
            errors.append(f"Mtx {self.Mtx} must have type str.")
        try:
            property_format.check_is_algo_msg_pack_encoded(self.Mtx)
        except SchemaError as e:
            errors.append(f"Mtx {self.Mtx}" " must have format AlgoMsgPackEncoded: {e}")
        if not isinstance(self.Addresses, list):
            errors.append(f"Addresses {self.Addresses} must have type list.")
        else:
            for elt in self.Addresses:
                if not isinstance(elt, str):
                    errors.append(f"elt {elt} of Addresses must have type str.")
                try:
                    property_format.check_is_algo_address_string_format(elt)
                except SchemaError as e:
                    errors.append(
                        f"elt {elt} of Addresses must have format AlgoAddressStringFormat; {e}"
                    )
        if not isinstance(self.Threshold, int):
            errors.append(f"Threshold {self.Threshold} must have type int.")
        if self.TypeName != "signandsubmit.mtx.algo.000":
            errors.append(
                f"Type requires TypeName of signandsubmit.mtx.algo.000, not {self.TypeName}."
            )

        return errors
