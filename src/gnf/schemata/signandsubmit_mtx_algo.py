"""signandsubmit.mtx.algo.000 type"""
from typing import List

from algosdk import encoding
from algosdk.future import transaction
from errors import SchemaError
from schemata.signandsubmit_mtx_algo_base import SignandsubmitMtxAlgoBase


class SignandsubmitMtxAlgo(SignandsubmitMtxAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making signandsubmit.mtx.algo.000 for {self}: {errors}"
            )

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
