"""exchange.tadeed.algo.010 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class ExchangeTadeedAlgo(NamedTuple):
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    NewTaDeedIdx: int  #
    OldDeedTransferMtx: str  #
    TaDaemonAddr: str  #
    TypeName: str = "exchange.tadeed.algo.010"

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
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except SchemaError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.NewTaDeedIdx, int):
            errors.append(f"NewTaDeedIdx {self.NewTaDeedIdx} must have type int.")
        if not isinstance(self.OldDeedTransferMtx, str):
            errors.append(
                f"OldDeedTransferMtx {self.OldDeedTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(self.OldDeedTransferMtx)
        except SchemaError as e:
            errors.append(
                f"OldDeedTransferMtx {self.OldDeedTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.TaDaemonAddr, str):
            errors.append(f"TaDaemonAddr {self.TaDaemonAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaDaemonAddr)
        except SchemaError as e:
            errors.append(
                f"TaDaemonAddr {self.TaDaemonAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "exchange.tadeed.algo.010":
            errors.append(
                f"Type requires TypeName of exchange.tadeed.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making exchange.tadeed.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "ExchangeTadeedAlgo"

    def hand_coded_errors(self):
        return []


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
