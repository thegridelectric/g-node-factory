"""Type heartbeat.a, version 100"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class HeartbeatA(BaseModel):
    TypeName: Literal["heartbeat.a"] = "heartbeat.a"
    Version: str = "100"

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class HeartbeatA_Maker:
    type_name = "heartbeat.a"
    version = "100"

    def __init__(self):

        self.tuple = HeartbeatA(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: HeartbeatA) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> HeartbeatA:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> HeartbeatA:
        d2 = dict(d)

        return HeartbeatA(
            TypeName=d2["TypeName"],
            Version="100",
        )
