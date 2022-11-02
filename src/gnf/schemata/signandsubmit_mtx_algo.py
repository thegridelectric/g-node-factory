"""Type signandsubmit.mtx.algo, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from algosdk import encoding
from algosdk.future import transaction
from pydantic import BaseModel
from pydantic import root_validator
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class SignandsubmitMtxAlgo(BaseModel):
    Mtx: str  #
    Addresses: List[str]
    Threshold: int  #
    SignerAddress: str  #
    TypeName: Literal["signandsubmit.mtx.algo"] = "signandsubmit.mtx.algo"
    Version: str = "000"

    _validator_mtx = predicate_validator(
        "Mtx", property_format.is_algo_msg_pack_encoded
    )

    @validator("Addresses")
    def _validator_addresses(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_algo_address_string_format(elt):
                raise ValueError(
                    f"failure of predicate is_algo_address_string_format() on elt {elt} of Addresses"
                )
        return v

    _validator_signer_address = predicate_validator(
        "SignerAddress", property_format.is_algo_address_string_format
    )

    @root_validator(pre=True)
    def _axioms_4(cls, v) -> Any:
        """Axiom 4: Decoded Mtx must have type MultisigTransaction."""
        mtx = encoding.future_msgpack_decode(v.get("Mtx", None))
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 4: Decoded Mtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )

        return v

    @root_validator
    def _axiom_5(cls, v) -> Any:
        """Axiom 5 (Internal Consistency): SignerAddress is one of the Addresses. Threshold is the
        threshold for the MultisigTransaction. Addresses are the list of addresses for the
         MultisigTransaction (order matters).
        """
        mtx = encoding.future_msgpack_decode(v.get("Mtx", None))
        SignerAddress = v.get("SignerAddress", None)
        Addresses = v.get("Addresses")
        Threshold = v.get("Threshold")
        if SignerAddress not in Addresses:
            raise ValueError(
                "Axiom 5 (Internal Consistency): SignerAddress must be one of the Addresses"
            )
        if Threshold != mtx.multisig.threshold:
            raise ValueError(
                "Axiom 5 (Internal Consistency): Threshold must equal "
                f"Mtx.multisig.threshold. {Threshold} != {mtx.multisig.threshold}"
            )
        mtx_addresses = list(
            map(lambda x: encoding.encode_address(x.public_key), mtx.multisig.subsigs)
        )
        if Addresses != mtx_addresses:
            raise ValueError(
                "Axiom 5 (Internal Consistency): Addresses must be the addresses for the"
                f"MultisigTransaction. {Addresses} != {mtx_addresses}"
            )
        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6 (Mtx threshold gets met): Once the SignerAddress signs, the Mtx meets its
        threshold of signatures."""
        mtx = encoding.future_msgpack_decode(v.get("Mtx", None))
        SignerAddress = v.get("SignerAddress", None)
        Threshold = v.get("Threshold")
        has_sig = list(
            map(
                lambda x: encoding.encode_address(x.public_key),
                filter(lambda x: x.signature is not None, mtx.multisig.subsigs),
            )
        )
        has_sig.append(SignerAddress)
        num_sigs_after_signing = len(set(has_sig))
        if num_sigs_after_signing < Threshold:
            raise ValueError(
                "Axiom 6 (Mtx threshold gets met): Once the SignerAddress signs, the Mtx meets"
                f"its threshold of signatures. Num sigs after signing {num_sigs_after_signing},"
                f" Threshold {Threshold}."
            )
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

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


class SignandsubmitMtxAlgo_Maker:
    type_name = "signandsubmit.mtx.algo"
    version = "000"

    def __init__(
        self, mtx: str, addresses: List[str], threshold: int, signer_address: str
    ):

        self.tuple = SignandsubmitMtxAlgo(
            Mtx=mtx,
            Addresses=addresses,
            Threshold=threshold,
            SignerAddress=signer_address,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: SignandsubmitMtxAlgo) -> str:
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
        d2 = dict(d)
        if "Mtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Mtx")
        if "Addresses" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Addresses")
        if "Threshold" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Threshold")
        if "SignerAddress" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignerAddress")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return SignandsubmitMtxAlgo(
            Mtx=d2["Mtx"],
            Addresses=d2["Addresses"],
            Threshold=d2["Threshold"],
            SignerAddress=d2["SignerAddress"],
            TypeName=d2["TypeName"],
            Version="000",
        )
