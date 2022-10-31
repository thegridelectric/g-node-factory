"""transfer.tavalidatorcert.algo.010 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class TransferTavalidatorcertAlgo(NamedTuple):
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
        except ValueError as e:
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
        except ValueError as e:
            errors.append(
                f"HalfSignedCertTransferMtx {self.HalfSignedCertTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if self.TypeName != "transfer.tavalidatorcert.algo.010":
            errors.append(
                f"Type requires TypeName of transfer.tavalidatorcert.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making transfer.tavalidatorcert.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferTavalidatorcertAlgo"

    def hand_coded_errors(self):
        return []


class TransferTavalidatorcertAlgo_Maker:
    type_name = "transfer.tavalidatorcert.algo.010"

    def __init__(self, validator_addr: str, half_signed_cert_transfer_mtx: str):

        gw_tuple = TransferTavalidatorcertAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedCertTransferMtx=half_signed_cert_transfer_mtx,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: TransferTavalidatorcertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferTavalidatorcertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferTavalidatorcertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "HalfSignedCertTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedCertTransferMtx")

        gw_tuple = TransferTavalidatorcertAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            HalfSignedCertTransferMtx=new_d["HalfSignedCertTransferMtx"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
