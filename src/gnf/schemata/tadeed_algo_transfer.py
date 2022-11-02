"""Type tadeed.algo.transfer, version 000"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedAlgoTransfer(BaseModel):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: Literal["tadeed.algo.transfer"] = "tadeed.algo.transfer"
    Version: str = "000"

    _validator_first_deed_transfer_mtx = predicate_validator(
        "FirstDeedTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    _validator_deed_validator_addr = predicate_validator(
        "DeedValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedAlgoTransfer_Maker:
    type_name = "tadeed.algo.transfer"
    version = "000"

    def __init__(
        self,
        first_deed_transfer_mtx: str,
        micro_lat: int,
        deed_validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lon: int,
    ):

        self.tuple = TadeedAlgoTransfer(
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            MicroLat=micro_lat,
            DeedValidatorAddr=deed_validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedAlgoTransfer) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedAlgoTransfer:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TadeedAlgoTransfer:
        d2 = dict(d)
        if "FirstDeedTransferMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FirstDeedTransferMtx")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "DeedValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DeedValidatorAddr")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedAlgoTransfer(
            FirstDeedTransferMtx=d2["FirstDeedTransferMtx"],
            MicroLat=d2["MicroLat"],
            DeedValidatorAddr=d2["DeedValidatorAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="000",
        )
