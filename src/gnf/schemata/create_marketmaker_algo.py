"""create.marketmaker.algo.001 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateMarketmakerAlgo(BaseModel):
    TypeName: Literal["create.marketmaker.algo"] = "create.marketmaker.algo"

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateMarketmakerAlgo_Maker:
    type_name = "create.marketmaker.algo"

    def __init__(self):

        self.tuple = CreateMarketmakerAlgo(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateMarketmakerAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateMarketmakerAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateMarketmakerAlgo:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return CreateMarketmakerAlgo(
            TypeName=d2["TypeName"],
        )
