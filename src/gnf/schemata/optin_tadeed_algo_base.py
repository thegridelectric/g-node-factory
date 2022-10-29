"""Base for optin.tadeed.algo.001 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class OptinTadeedAlgoBase(NamedTuple):
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TaOwnerAddr: str  #
    TaDaemonAddr: str  #
    TypeName: str = "optin.tadeed.algo.001"

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
        if not isinstance(self.NewDeedOptInMtx, str):
            errors.append(f"NewDeedOptInMtx {self.NewDeedOptInMtx} must have type str.")
        try:
            property_format.check_is_algo_msg_pack_encoded(self.NewDeedOptInMtx)
        except SchemaError as e:
            errors.append(
                f"NewDeedOptInMtx {self.NewDeedOptInMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
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
        if not isinstance(self.TaDaemonAddr, str):
            errors.append(f"TaDaemonAddr {self.TaDaemonAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaDaemonAddr)
        except SchemaError as e:
            errors.append(
                f"TaDaemonAddr {self.TaDaemonAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "optin.tadeed.algo.001":
            errors.append(
                f"Type requires TypeName of optin.tadeed.algo.001, not {self.TypeName}."
            )

        return errors
