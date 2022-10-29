"""Makes signandsubmit.mtx.algo.000 type"""
import json
from typing import List

from errors import SchemaError
from schemata.signandsubmit_mtx_algo import SignandsubmitMtxAlgo


class SignandsubmitMtxAlgo_Maker:
    type_name = "signandsubmit.mtx.algo.000"

    def __init__(
        self, signer_address: str, mtx: str, addresses: List[str], threshold: int
    ):

        gw_tuple = SignandsubmitMtxAlgo(
            SignerAddress=signer_address,
            Mtx=mtx,
            Addresses=addresses,
            Threshold=threshold,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: SignandsubmitMtxAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> SignandsubmitMtxAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> SignandsubmitMtxAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "SignerAddress" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing SignerAddress")
        if "Mtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Mtx")
        if "Addresses" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Addresses")
        if "Threshold" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Threshold")

        gw_tuple = SignandsubmitMtxAlgo(
            TypeName=new_d["TypeName"],
            SignerAddress=new_d["SignerAddress"],
            Mtx=new_d["Mtx"],
            Addresses=new_d["Addresses"],
            Threshold=new_d["Threshold"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
