"""Type tadeed.algo.exchange, version 001"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedAlgoExchange(BaseModel):
    OldTaDeedIdx: int  #
    TaDaemonAddr: str  #
    ValidatorAddr: str  #
    SignedNewDeedTransferTxn: str  #
    TypeName: Literal["tadeed.algo.exchange"] = "tadeed.algo.exchange"
    Version: str = "001"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_signed_new_deed_transfer_txn = predicate_validator(
        "SignedNewDeedTransferTxn", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedAlgoExchange_Maker:
    type_name = "tadeed.algo.exchange"
    version = "001"

    def __init__(
        self,
        old_ta_deed_idx: int,
        ta_daemon_addr: str,
        validator_addr: str,
        signed_new_deed_transfer_txn: str,
    ):

        self.tuple = TadeedAlgoExchange(
            OldTaDeedIdx=old_ta_deed_idx,
            TaDaemonAddr=ta_daemon_addr,
            ValidatorAddr=validator_addr,
            SignedNewDeedTransferTxn=signed_new_deed_transfer_txn,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedAlgoExchange) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedAlgoExchange:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TadeedAlgoExchange:
        d2 = dict(d)
        if "OldTaDeedIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OldTaDeedIdx")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "SignedNewDeedTransferTxn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignedNewDeedTransferTxn")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedAlgoExchange(
            OldTaDeedIdx=d2["OldTaDeedIdx"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            SignedNewDeedTransferTxn=d2["SignedNewDeedTransferTxn"],
            TypeName=d2["TypeName"],
            Version="001",
        )
