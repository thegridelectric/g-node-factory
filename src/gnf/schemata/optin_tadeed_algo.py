"""optin.tadeed.algo.001 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class OptinTadeedAlgo(NamedTuple):
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TaOwnerAddr: str  #
    TaDaemonAddr: str  #
    TypeName: str = "optin.tadeed.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except ValueError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.NewDeedOptInMtx, str):
            errors.append(f"NewDeedOptInMtx {self.NewDeedOptInMtx} must have type str.")
        try:
            property_format.check_is_algo_msg_pack_encoded(self.NewDeedOptInMtx)
        except ValueError as e:
            errors.append(
                f"NewDeedOptInMtx {self.NewDeedOptInMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except ValueError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.TaDaemonAddr, str):
            errors.append(f"TaDaemonAddr {self.TaDaemonAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaDaemonAddr)
        except ValueError as e:
            errors.append(
                f"TaDaemonAddr {self.TaDaemonAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "optin.tadeed.algo.001":
            errors.append(
                f"Type requires TypeName of optin.tadeed.algo.001, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making optin.tadeed.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "OptinTadeedAlgo"

    def hand_coded_errors(self):
        return []


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
