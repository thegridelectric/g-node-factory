"""Makes create.tadeed.algo.010 type"""
import json

from errors import SchemaError
from schemata.create_tadeed_algo import CreateTadeedAlgo


class CreateTadeedAlgo_Maker:
    type_name = "create.tadeed.algo.010"

    def __init__(self, validator_addr: str, half_signed_deed_creation_mtx: str):

        gw_tuple = CreateTadeedAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedDeedCreationMtx=half_signed_deed_creation_mtx,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "HalfSignedDeedCreationMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedDeedCreationMtx")

        gw_tuple = CreateTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            HalfSignedDeedCreationMtx=new_d["HalfSignedDeedCreationMtx"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
