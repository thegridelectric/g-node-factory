"""transfer.tavalidatorcert.algo.010 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TransferTavalidatorcertAlgo(BaseModel):
    ValidatorAddr: str  #
    HalfSignedCertTransferMtx: str  #
    TypeName: Literal["transfer.tavalidatorcert.algo"] = "transfer.tavalidatorcert.algo"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_cert_transfer_mtx = predicate_validator(
        "HalfSignedCertTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TransferTavalidatorcertAlgo_Maker:
    type_name = "transfer.tavalidatorcert.algo"

    def __init__(self, validator_addr: str, half_signed_cert_transfer_mtx: str):

        self.tuple = TransferTavalidatorcertAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedCertTransferMtx=half_signed_cert_transfer_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TransferTavalidatorcertAlgo) -> str:
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
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TransferTavalidatorcertAlgo(
            TypeName=d2["TypeName"],
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedCertTransferMtx=d2["HalfSignedCertTransferMtx"],
        )
