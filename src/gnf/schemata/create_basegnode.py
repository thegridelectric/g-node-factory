"""create.basegnode.010 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class CreateBasegnode(BaseModel):
    TypeName: Literal["create.basegnode"] = "create.basegnode"

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class CreateBasegnode_Maker:
    type_name = "create.basegnode"

    def __init__(self):

        self.tuple = CreateBasegnode(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: CreateBasegnode) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateBasegnode:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateBasegnode:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return CreateBasegnode(
            TypeName=d2["TypeName"],
        )
