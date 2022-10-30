"""transfer.tadeed.algo.020 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class TransferTadeedAlgo(NamedTuple):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: str = "transfer.tadeed.algo.020"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.FirstDeedTransferMtx, str):
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(self.FirstDeedTransferMtx)
        except SchemaError as e:
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.DeedValidatorAddr, str):
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.DeedValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
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
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except SchemaError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if self.TypeName != "transfer.tadeed.algo.020":
            errors.append(
                f"Type requires TypeName of transfer.tadeed.algo.020, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making transfer.tadeed.algo.020 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferTadeedAlgo"

    def hand_coded_errors(self):
        return []


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
