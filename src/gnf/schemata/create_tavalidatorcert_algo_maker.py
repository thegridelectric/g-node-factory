"""Makes create.tavalidatorcert.algo.010 type"""
import json

from errors import SchemaError
from schemata.create_tavalidatorcert_algo import CreateTavalidatorcertAlgo


class CreateTavalidatorcertAlgo_Maker:
    type_name = "create.tavalidatorcert.algo.010"

    def __init__(self, half_signed_cert_creation_mtx: str, validator_addr: str):

        gw_tuple = CreateTavalidatorcertAlgo(
            HalfSignedCertCreationMtx=half_signed_cert_creation_mtx,
            ValidatorAddr=validator_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTavalidatorcertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTavalidatorcertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTavalidatorcertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "HalfSignedCertCreationMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedCertCreationMtx")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")

        gw_tuple = CreateTavalidatorcertAlgo(
            TypeName=new_d["TypeName"],
            HalfSignedCertCreationMtx=new_d["HalfSignedCertCreationMtx"],
            ValidatorAddr=new_d["ValidatorAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple