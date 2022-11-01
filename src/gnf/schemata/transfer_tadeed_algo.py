"""Type transfer.tadeed.algo, version 020"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TransferTadeedAlgo(BaseModel):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: Literal["transfer.tadeed.algo"] = "transfer.tadeed.algo"
    Version: str = "020"

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


class TransferTadeedAlgo_Maker:
    type_name = "transfer.tadeed.algo"
    version = "020"

    def __init__(
        self,
        first_deed_transfer_mtx: str,
        micro_lat: int,
        deed_validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lon: int,
    ):

        self.tuple = TransferTadeedAlgo(
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            MicroLat=micro_lat,
            DeedValidatorAddr=deed_validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TransferTadeedAlgo) -> str:
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
        d2 = dict(d)

        return TransferTadeedAlgo(
            FirstDeedTransferMtx=d2["FirstDeedTransferMtx"],
            MicroLat=d2["MicroLat"],
            DeedValidatorAddr=d2["DeedValidatorAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="020",
        )
