"""Makes transfer.tavalidatorcert.algo.010 type"""
import json

from errors import SchemaError
from schemata.transfer_tavalidatorcert_algo import TransferTavalidatorcertAlgo


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
