"""Type signandsubmit.mtx.algo, version 000"""
import json
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class SignandsubmitMtxAlgo(BaseModel):
    SignerAddress: str  #
    Mtx: str  #
    Addresses: List[str]
    Threshold: int  #
    TypeName: Literal["signandsubmit.mtx.algo"] = "signandsubmit.mtx.algo"
    Version: str = "000"

    _validator_signer_address = predicate_validator(
        "SignerAddress", property_format.is_algo_address_string_format
    )

    _validator_mtx = predicate_validator(
        "Mtx", property_format.is_algo_msg_pack_encoded
    )

    @validator("Addresses")
    def _validator_addresses(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_algo_address_string_format(elt):
                raise ValueError(
                    f"failure of predicate is_algo_address_string_format() on elt {elt} of Addresses"
                )
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class SignandsubmitMtxAlgo_Maker:
    type_name = "signandsubmit.mtx.algo"
    version = "000"

    def __init__(
        self, signer_address: str, mtx: str, addresses: List[str], threshold: int
    ):

        self.tuple = SignandsubmitMtxAlgo(
            SignerAddress=signer_address,
            Mtx=mtx,
            Addresses=addresses,
            Threshold=threshold,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: SignandsubmitMtxAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> SignandsubmitMtxAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> SignandsubmitMtxAlgo:
        d2 = dict(d)

        return SignandsubmitMtxAlgo(
            SignerAddress=d2["SignerAddress"],
            Mtx=d2["Mtx"],
            Addresses=d2["Addresses"],
            Threshold=d2["Threshold"],
            TypeName=d2["TypeName"],
            Version="000",
        )
