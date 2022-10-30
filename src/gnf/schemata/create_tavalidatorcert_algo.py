"""create.tavalidatorcert.algo.010 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class CreateTavalidatorcertAlgo(NamedTuple):
    HalfSignedCertCreationMtx: str  #
    ValidatorAddr: str  #
    TypeName: str = "create.tavalidatorcert.algo.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.HalfSignedCertCreationMtx, str):
            errors.append(
                f"HalfSignedCertCreationMtx {self.HalfSignedCertCreationMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedCertCreationMtx
            )
        except SchemaError as e:
            errors.append(
                f"HalfSignedCertCreationMtx {self.HalfSignedCertCreationMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"ValidatorAddr {self.ValidatorAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "create.tavalidatorcert.algo.010":
            errors.append(
                f"Type requires TypeName of create.tavalidatorcert.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.tavalidatorcert.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateTavalidatorcertAlgo"

    def hand_coded_errors(self):
        return []


class CreateTavalidatorcertAlgo_Maker:
    type_name = "create.tavalidatorcert.algo.010"

    def __init__(self, half_signed_cert_creation_mtx: str, validator_addr: str):

        gw_tuple = CreateTavalidatorcertAlgo(
            HalfSignedCertCreationMtx=half_signed_cert_creation_mtx,
            ValidatorAddr=validator_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateTavalidatorcertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateTavalidatorcertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateTavalidatorcertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "HalfSignedCertCreationMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedCertCreationMtx")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")

        gw_tuple = CreateTavalidatorcertAlgo(
            TypeName=new_d["TypeName"],
            HalfSignedCertCreationMtx=new_d["HalfSignedCertCreationMtx"],
            ValidatorAddr=new_d["ValidatorAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
