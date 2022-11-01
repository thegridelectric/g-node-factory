"""Type create.tatradingrights.algo, version 001"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateTatradingrightsAlgo(BaseModel):
    TypeName: Literal["create.tatradingrights.algo"] = "create.tatradingrights.algo"
    Version: str = "001"

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateTatradingrightsAlgo_Maker:
    type_name = "create.tatradingrights.algo"
    version = "001"

    def __init__(self):

        self.tuple = CreateTatradingrightsAlgo(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateTatradingrightsAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTatradingrightsAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTatradingrightsAlgo:
        d2 = dict(d)

        return CreateTatradingrightsAlgo(
            TypeName=d2["TypeName"],
            Version="001",
        )
