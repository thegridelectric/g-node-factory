"""Makes exchange.tadeed.algo.010 type"""
import json

from errors import SchemaError
from schemata.exchange_tadeed_algo import ExchangeTadeedAlgo


class ExchangeTadeedAlgo_Maker:
    type_name = "exchange.tadeed.algo.010"

    def __init__(
        self,
        validator_addr: str,
        ta_owner_addr: str,
        new_ta_deed_idx: int,
        old_deed_transfer_mtx: str,
        ta_daemon_addr: str,
    ):

        gw_tuple = ExchangeTadeedAlgo(
            ValidatorAddr=validator_addr,
            TaOwnerAddr=ta_owner_addr,
            NewTaDeedIdx=new_ta_deed_idx,
            OldDeedTransferMtx=old_deed_transfer_mtx,
            TaDaemonAddr=ta_daemon_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: ExchangeTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> ExchangeTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> ExchangeTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "NewTaDeedIdx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing NewTaDeedIdx")
        if "OldDeedTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing OldDeedTransferMtx")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")

        gw_tuple = ExchangeTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            NewTaDeedIdx=new_d["NewTaDeedIdx"],
            OldDeedTransferMtx=new_d["OldDeedTransferMtx"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
