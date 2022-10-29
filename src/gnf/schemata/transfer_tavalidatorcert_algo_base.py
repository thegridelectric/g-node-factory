"""Base for transfer.tavalidatorcert.algo.010 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class TransferTavalidatorcertAlgoBase(NamedTuple):
    ValidatorAddr: str  #
    HalfSignedCertTransferMtx: str  #
    TypeName: str = "transfer.tavalidatorcert.algo.010"

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
        if not isinstance(self.HalfSignedCertTransferMtx, str):
            errors.append(
                f"HalfSignedCertTransferMtx {self.HalfSignedCertTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedCertTransferMtx
            )
        except SchemaError as e:
            errors.append(
                f"HalfSignedCertTransferMtx {self.HalfSignedCertTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if self.TypeName != "transfer.tavalidatorcert.algo.010":
            errors.append(
                f"Type requires TypeName of transfer.tavalidatorcert.algo.010, not {self.TypeName}."
            )

        return errors
