"""Makes heartbeat.a.100 type"""
import json

from errors import SchemaError
from schemata.heartbeat_a import HeartbeatA


class HeartbeatA_Maker:
    type_name = "heartbeat.a.100"

    def __init__(self):

        gw_tuple = HeartbeatA(
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: HeartbeatA) -> bytes:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: bytes) -> HeartbeatA:
        try:
            d = json.loads(str(t, "utf-8"))
        except TypeError:
            raise SchemaError("Type must utf-8 encoded dict!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> HeartbeatA:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")

        gw_tuple = HeartbeatA(
            TypeName=new_d["TypeName"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
