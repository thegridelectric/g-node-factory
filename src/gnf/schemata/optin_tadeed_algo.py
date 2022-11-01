"""optin.tadeed.algo.001 type"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class OptinTadeedAlgo(BaseModel):
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TaOwnerAddr: str  #
    TaDaemonAddr: str  #
    TypeName: Literal["optin.tadeed.algo"] = "optin.tadeed.algo"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_new_deed_opt_in_mtx = predicate_validator(
        "NewDeedOptInMtx", property_format.is_algo_msg_pack_encoded
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo"

    def __init__(
        self,
        validator_addr: str,
        new_deed_opt_in_mtx: str,
        ta_owner_addr: str,
        ta_daemon_addr: str,
    ):

        self.tuple = OptinTadeedAlgo(
            ValidatorAddr=validator_addr,
            NewDeedOptInMtx=new_deed_opt_in_mtx,
            TaOwnerAddr=ta_owner_addr,
            TaDaemonAddr=ta_daemon_addr,
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
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return OptinTadeedAlgo(
            TypeName=d2["TypeName"],
            ValidatorAddr=d2["ValidatorAddr"],
            NewDeedOptInMtx=d2["NewDeedOptInMtx"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
        )
