"""Base for transfer.tadeed.algo.020 """


import json
from typing import List
from typing import NamedTuple

import property_format
from errors import SchemaError


class TransferTadeedAlgoBase(NamedTuple):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: str = "transfer.tadeed.algo.020"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.FirstDeedTransferMtx, str):
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(self.FirstDeedTransferMtx)
        except SchemaError as e:
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.DeedValidatorAddr, str):
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.DeedValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr}"
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
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except SchemaError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if self.TypeName != "transfer.tadeed.algo.020":
            errors.append(
                f"Type requires TypeName of transfer.tadeed.algo.020, not {self.TypeName}."
            )

        return errors
