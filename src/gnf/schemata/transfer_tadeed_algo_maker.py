"""Makes transfer.tadeed.algo.020 type"""
import json

from errors import SchemaError
from schemata.transfer_tadeed_algo import TransferTadeedAlgo


class TransferTadeedAlgo_Maker:
    type_name = "transfer.tadeed.algo.020"

    def __init__(
        self,
        first_deed_transfer_mtx: str,
        micro_lat: int,
        deed_validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lon: int,
    ):

        gw_tuple = TransferTadeedAlgo(
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            MicroLat=micro_lat,
            DeedValidatorAddr=deed_validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLon=micro_lon,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: TransferTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "FirstDeedTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FirstDeedTransferMtx")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "DeedValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DeedValidatorAddr")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")

        gw_tuple = TransferTadeedAlgo(
            TypeName=new_d["TypeName"],
            FirstDeedTransferMtx=new_d["FirstDeedTransferMtx"],
            MicroLat=new_d["MicroLat"],
            DeedValidatorAddr=new_d["DeedValidatorAddr"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            MicroLon=new_d["MicroLon"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
