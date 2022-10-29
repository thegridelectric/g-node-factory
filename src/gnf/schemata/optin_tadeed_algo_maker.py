"""Makes optin.tadeed.algo.001 type"""
import json

from errors import SchemaError
from schemata.optin_tadeed_algo import OptinTadeedAlgo


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo.001"

    def __init__(
        self,
        validator_addr: str,
        new_deed_opt_in_mtx: str,
        ta_owner_addr: str,
        ta_daemon_addr: str,
    ):

        gw_tuple = OptinTadeedAlgo(
            ValidatorAddr=validator_addr,
            NewDeedOptInMtx=new_deed_opt_in_mtx,
            TaOwnerAddr=ta_owner_addr,
            TaDaemonAddr=ta_daemon_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: OptinTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> OptinTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> OptinTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "NewDeedOptInMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing NewDeedOptInMtx")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")

        gw_tuple = OptinTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            NewDeedOptInMtx=new_d["NewDeedOptInMtx"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
