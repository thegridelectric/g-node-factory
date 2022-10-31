"""create.tadeed.algo.010 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class CreateTadeedAlgo(NamedTuple):
    ValidatorAddr: str  #
    HalfSignedDeedCreationMtx: str  #
    TypeName: str = "create.tadeed.algo.010"

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
        if not isinstance(self.HalfSignedDeedCreationMtx, str):
            errors.append(
                f"HalfSignedDeedCreationMtx {self.HalfSignedDeedCreationMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedDeedCreationMtx
            )
        except ValueError as e:
            errors.append(
                f"HalfSignedDeedCreationMtx {self.HalfSignedDeedCreationMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if self.TypeName != "create.tadeed.algo.010":
            errors.append(
                f"Type requires TypeName of create.tadeed.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.tadeed.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateTadeedAlgo"

    def hand_coded_errors(self):
        return []


class CreateTadeedAlgo_Maker:
    type_name = "create.tadeed.algo.010"

    def __init__(self, validator_addr: str, half_signed_deed_creation_mtx: str):

        gw_tuple = CreateTadeedAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedDeedCreationMtx=half_signed_deed_creation_mtx,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "HalfSignedDeedCreationMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedDeedCreationMtx")

        gw_tuple = CreateTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            HalfSignedDeedCreationMtx=new_d["HalfSignedDeedCreationMtx"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
