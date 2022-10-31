"""signandsubmit.mtx.algo.000 type"""

import json
from typing import List
from typing import NamedTuple

import gnf.property_format as property_format
from gnf.errors import SchemaError


class SignandsubmitMtxAlgo(NamedTuple):
    SignerAddress: str  #
    Mtx: str  #
    Addresses: List[str]
    Threshold: int  #
    TypeName: str = "signandsubmit.mtx.algo.000"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.SignerAddress, str):
            errors.append(f"SignerAddress {self.SignerAddress} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.SignerAddress)
        except ValueError as e:
            errors.append(
                f"SignerAddress {self.SignerAddress}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.Mtx, str):
            errors.append(f"Mtx {self.Mtx} must have type str.")
        try:
            property_format.check_is_algo_msg_pack_encoded(self.Mtx)
        except ValueError as e:
            errors.append(f"Mtx {self.Mtx}" " must have format AlgoMsgPackEncoded: {e}")
        if not isinstance(self.Addresses, list):
            errors.append(f"Addresses {self.Addresses} must have type list.")
        else:
            for elt in self.Addresses:
                if not isinstance(elt, str):
                    errors.append(f"elt {elt} of Addresses must have type str.")
                try:
                    property_format.check_is_algo_address_string_format(elt)
                except ValueError as e:
                    errors.append(
                        f"elt {elt} of Addresses must have format AlgoAddressStringFormat; {e}"
                    )
        if not isinstance(self.Threshold, int):
            errors.append(f"Threshold {self.Threshold} must have type int.")
        if self.TypeName != "signandsubmit.mtx.algo.000":
            errors.append(
                f"Type requires TypeName of signandsubmit.mtx.algo.000, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making signandsubmit.mtx.algo.000 for {self}: {errors}"
            )

    def __repr__(self):
        return "SignandsubmitMtxAlgo"

    def hand_coded_errors(self):
        return []


class SignandsubmitMtxAlgo_Maker:
    type_name = "signandsubmit.mtx.algo.000"

    def __init__(
        self, signer_address: str, mtx: str, addresses: List[str], threshold: int
    ):

        gw_tuple = SignandsubmitMtxAlgo(
            SignerAddress=signer_address,
            Mtx=mtx,
            Addresses=addresses,
            Threshold=threshold,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: SignandsubmitMtxAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> SignandsubmitMtxAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> SignandsubmitMtxAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "SignerAddress" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing SignerAddress")
        if "Mtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Mtx")
        if "Addresses" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Addresses")
        if "Threshold" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing Threshold")

        gw_tuple = SignandsubmitMtxAlgo(
            TypeName=new_d["TypeName"],
            SignerAddress=new_d["SignerAddress"],
            Mtx=new_d["Mtx"],
            Addresses=new_d["Addresses"],
            Threshold=new_d["Threshold"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
