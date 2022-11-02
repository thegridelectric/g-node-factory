"""Type optin.tadeed.algo, version 000"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class OptinTadeedAlgo(BaseModel):
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TypeName: Literal["optin.tadeed.algo"] = "optin.tadeed.algo"
    Version: str = "000"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_new_deed_opt_in_mtx = predicate_validator(
        "NewDeedOptInMtx", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo"
    version = "000"

    def __init__(
        self,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        validator_addr: str,
        new_deed_opt_in_mtx: str,
    ):

        self.tuple = OptinTadeedAlgo(
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            ValidatorAddr=validator_addr,
            NewDeedOptInMtx=new_deed_opt_in_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: OptinTadeedAlgo) -> str:
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
        d2 = dict(d)
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "NewDeedOptInMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NewDeedOptInMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return OptinTadeedAlgo(
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            NewDeedOptInMtx=d2["NewDeedOptInMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
