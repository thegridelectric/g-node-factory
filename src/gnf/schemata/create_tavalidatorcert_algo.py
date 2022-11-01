"""Type create.tavalidatorcert.algo, version 010"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateTavalidatorcertAlgo(BaseModel):
    HalfSignedCertCreationMtx: str  #
    ValidatorAddr: str  #
    TypeName: Literal["create.tavalidatorcert.algo"] = "create.tavalidatorcert.algo"
    Version: str = "010"

    _validator_half_signed_cert_creation_mtx = predicate_validator(
        "HalfSignedCertCreationMtx", property_format.is_algo_msg_pack_encoded
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateTavalidatorcertAlgo_Maker:
    type_name = "create.tavalidatorcert.algo"
    version = "010"

    def __init__(self, half_signed_cert_creation_mtx: str, validator_addr: str):

        self.tuple = CreateTavalidatorcertAlgo(
            HalfSignedCertCreationMtx=half_signed_cert_creation_mtx,
            ValidatorAddr=validator_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateTavalidatorcertAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTavalidatorcertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTavalidatorcertAlgo:
        d2 = dict(d)

        return CreateTavalidatorcertAlgo(
            HalfSignedCertCreationMtx=d2["HalfSignedCertCreationMtx"],
            ValidatorAddr=d2["ValidatorAddr"],
            TypeName=d2["TypeName"],
            Version="010",
        )
