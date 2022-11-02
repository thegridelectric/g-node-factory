"""Type basegnodes.get, version 000"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

from gnf.errors import SchemaError


class BasegnodesGet(BaseModel):
    TypeName: Literal["basegnodes.get"] = "basegnodes.get"
    Version: str = "000"

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodesGet_Maker:
    type_name = "basegnodes.get"
    version = "000"

    def __init__(self):

        self.tuple = BasegnodesGet(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodesGet) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodesGet:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> BasegnodesGet:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodesGet(
            TypeName=d2["TypeName"],
            Version="000",
        )
