"""create.tadeed.algo.010 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateTadeedAlgo(BaseModel):
    ValidatorAddr: str  #
    HalfSignedDeedCreationMtx: str  #
    TypeName: Literal["create.tadeed.algo"] = "create.tadeed.algo"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_deed_creation_mtx = predicate_validator(
        "HalfSignedDeedCreationMtx", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateTadeedAlgo_Maker:
    type_name = "create.tadeed.algo"

    def __init__(self, validator_addr: str, half_signed_deed_creation_mtx: str):

        self.tuple = CreateTadeedAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedDeedCreationMtx=half_signed_deed_creation_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateTadeedAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTadeedAlgo:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return CreateTadeedAlgo(
            TypeName=d2["TypeName"],
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedDeedCreationMtx=d2["HalfSignedDeedCreationMtx"],
        )
