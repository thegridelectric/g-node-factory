"""Type debug.tc.reinitialize.time, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class DebugTcReinitializeTime(BaseModel):
    ToGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    FromGNodeAlias: str  #
    TypeName: Literal["debug.tc.reinitialize.time"] = "debug.tc.reinitialize.time"
    Version: str = "000"

    _validator_to_g_node_alias = predicate_validator(
        "ToGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class DebugTcReinitializeTime_Maker:
    type_name = "debug.tc.reinitialize.time"
    version = "000"

    def __init__(
        self, to_g_node_alias: str, from_g_node_instance_id: str, from_g_node_alias: str
    ):

        self.tuple = DebugTcReinitializeTime(
            ToGNodeAlias=to_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            FromGNodeAlias=from_g_node_alias,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: DebugTcReinitializeTime) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> DebugTcReinitializeTime:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> DebugTcReinitializeTime:
        d2 = dict(d)
        if "ToGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ToGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return DebugTcReinitializeTime(
            ToGNodeAlias=d2["ToGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            FromGNodeAlias=d2["FromGNodeAlias"],
            TypeName=d2["TypeName"],
            Version="000",
        )
