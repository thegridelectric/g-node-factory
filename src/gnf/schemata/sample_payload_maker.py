"""Makes sample.payload.100 type"""
import json

from errors import SchemaError
from schemata.sample_payload import SamplePayload


class SamplePayload_Maker:
    type_name = "sample.payload.100"

    def __init__(
        self,
        sampleAddr: str,
    ):

        gw_tuple = SamplePayload(
            sampleAddr=sampleAddr,
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: SamplePayload) -> bytes:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> SamplePayload:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must utf-8 encoded dict!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> SamplePayload:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "sampleAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing sampleAddr")

        gw_tuple = SamplePayload(
            TypeName=new_d["TypeName"],
            sampleAddr=new_d["sampleAddr"],
        )
        gw_tuple.check_for_errors()
        return gw_tuple
