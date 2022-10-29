"""Makes create.tatradingrights.algo.001 type"""
import json

from errors import SchemaError
from schemata.create_tatradingrights_algo import CreateTatradingrightsAlgo


class CreateTatradingrightsAlgo_Maker:
    type_name = "create.tatradingrights.algo.001"

    def __init__(self):

        gw_tuple = CreateTatradingrightsAlgo(
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTatradingrightsAlgo) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")

        gw_tuple = CreateTatradingrightsAlgo(
            TypeName=new_d["TypeName"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
