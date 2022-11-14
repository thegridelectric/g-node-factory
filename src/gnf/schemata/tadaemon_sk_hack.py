"""Type tadaemon.sk.hack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadaemonSkHack(BaseModel):
    TaOwnerAddr: str  #
    TaDaemonSk: str  #
    TypeName: Literal["tadaemon.sk.hack"] = "tadaemon.sk.hack"
    Version: str = "000"

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadaemonSkHack_Maker:
    type_name = "tadaemon.sk.hack"
    version = "000"

    def __init__(self, ta_owner_addr: str, ta_daemon_sk: str):

        self.tuple = TadaemonSkHack(
            TaOwnerAddr=ta_owner_addr,
            TaDaemonSk=ta_daemon_sk,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadaemonSkHack) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadaemonSkHack:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> TadaemonSkHack:
        d2 = dict(d)
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "TaDaemonSk" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonSk")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadaemonSkHack(
            TaOwnerAddr=d2["TaOwnerAddr"],
            TaDaemonSk=d2["TaDaemonSk"],
            TypeName=d2["TypeName"],
            Version="000",
        )
