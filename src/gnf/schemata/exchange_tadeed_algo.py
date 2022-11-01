"""Type exchange.tadeed.algo, version 010"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class ExchangeTadeedAlgo(BaseModel):
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    NewTaDeedIdx: int  #
    OldDeedTransferMtx: str  #
    TaDaemonAddr: str  #
    TypeName: Literal["exchange.tadeed.algo"] = "exchange.tadeed.algo"
    Version: str = "010"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_old_deed_transfer_mtx = predicate_validator(
        "OldDeedTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class ExchangeTadeedAlgo_Maker:
    type_name = "exchange.tadeed.algo"
    version = "010"

    def __init__(
        self,
        validator_addr: str,
        ta_owner_addr: str,
        new_ta_deed_idx: int,
        old_deed_transfer_mtx: str,
        ta_daemon_addr: str,
    ):

        self.tuple = ExchangeTadeedAlgo(
            ValidatorAddr=validator_addr,
            TaOwnerAddr=ta_owner_addr,
            NewTaDeedIdx=new_ta_deed_idx,
            OldDeedTransferMtx=old_deed_transfer_mtx,
            TaDaemonAddr=ta_daemon_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: ExchangeTadeedAlgo) -> str:
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
        d2 = dict(d)

        return ExchangeTadeedAlgo(
            ValidatorAddr=d2["ValidatorAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            NewTaDeedIdx=d2["NewTaDeedIdx"],
            OldDeedTransferMtx=d2["OldDeedTransferMtx"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TypeName=d2["TypeName"],
            Version="010",
        )
