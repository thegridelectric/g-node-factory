"""signandsubmit.mtx.algo.000 type"""

import json
from typing import List
from typing import NamedTuple

from algosdk import encoding
from algosdk.future import transaction

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

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making signandsubmit.mtx.algo.000 for {self}: {errors}"
            )

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

    def __repr__(self):
        r = "SignandsubmitMtxAlgo"
        r += f"\n       TypeName: {self.TypeName}"
        r += f"\n       SignerAddress: ..{self.SignerAddress[-6:]}"
        r += f"\n       Threshold: {self.Threshold}"
        short_addr_list = list(map(lambda x: f"..{x[-6:]}", self.Addresses))
        r += f"\n       Addresses: {short_addr_list}"
        mtx = encoding.future_msgpack_decode(self.Mtx)
        mtx_addresses = list(
            map(lambda x: encoding.encode_address(x.public_key), mtx.multisig.subsigs)
        )
        mtx_short_addr_list = list(map(lambda x: f"..{x[-6:]}", mtx_addresses))
        r += "\n       Mtx:"

        r += f"\n         - addresses={mtx_short_addr_list}"
        r += f"\n         - threshold={mtx.multisig.threshold}"
        return r

    def _axiom_4_errors(self) -> List[str]:
        """Axiom 4 (Mtx is MultisigTransaction): Once decoded, Mtx is a MultisigTransaction"""
        errors = []
        mtx = encoding.future_msgpack_decode(self.Mtx)
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                "Axiom 4 (Mtx is MultisigTransaction): Once decoded, Mtx is a"
                f"MultisigTransaction. Got {type(mtx)}"
            )
        return errors

    def _axiom_5_errors(self) -> List[str]:
        """Axiom 5 (Internal Consistency): SignerAddress is one of the Addresses. Threshold is the
        threshold for the MultisigTransaction. Addresses are the list of addresses for the
         MultisigTransaction (order matters).
        """
        errors = []
        mtx = encoding.future_msgpack_decode(self.Mtx)
        if self.SignerAddress not in self.Addresses:
            errors.append(
                "Axiom 5 (Internal Consistency): SignerAddress must be one of the Addresses"
            )
        if self.Threshold != mtx.multisig.threshold:
            errors.append(
                "Axiom 5 (Internal Consistency): Threshold must equal "
                f"Mtx.multisig.threshold. {self.Threshold} != {mtx.multisig.threshold}"
            )
        mtx_addresses = list(
            map(lambda x: encoding.encode_address(x.public_key), mtx.multisig.subsigs)
        )
        if self.Addresses != mtx_addresses:
            errors.append(
                "Axiom 5 (Internal Consistency): Addresses must be the addresses for the"
                f"MultisigTransaction. {self.Addresses} != {mtx_addresses}"
            )
        return errors

    def _axiom_6_errors(self) -> List[str]:
        """Axiom 6 (Mtx threshold gets met): Once the SignerAddress signs, the Mtx meets its
        threshold of signatures."""
        errors = []
        mtx = encoding.future_msgpack_decode(self.Mtx)
        has_sig = list(
            map(
                lambda x: encoding.encode_address(x.public_key),
                filter(lambda x: x.signature is not None, mtx.multisig.subsigs),
            )
        )
        has_sig.append(self.SignerAddress)
        num_sigs_after_signing = len(set(has_sig))
        if num_sigs_after_signing < self.Threshold:
            errors.append(
                "Axiom 6 (Mtx threshold gets met): Once the SignerAddress signs, the Mtx meets"
                f"its threshold of signatures. Num sigs after signing {num_sigs_after_signing},"
                f" Threshold {self.Threshold}."
            )
        return errors

    def axiom_errors(self):
        errors = []
        errors += self._axiom_4_errors()
        if len(errors) != 0:
            return errors
        errors += self._axiom_5_errors()
        errors += self._axiom_6_errors()
        return errors


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
