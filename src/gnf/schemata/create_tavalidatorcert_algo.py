"""create.tavalidatorcert.algo.010 type"""
from typing import List
from typing import OrderedDict

import algo_utils
import algosdk
import api_utils
import config
from algosdk import encoding
from algosdk.future import transaction
from errors import SchemaError
from schemata.create_tavalidatorcert_algo_base import CreateTavalidatorcertAlgoBase


class CreateTavalidatorcertAlgo(CreateTavalidatorcertAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.tavalidatorcert.algo.010: {errors}"
            )

    def __repr__(self):
        r = "CreateTavalidatorcertAlgo"
        r += f"\n   API TypeName: {self.TypeName}"
        r += f"\n   ValidatorAddr: {self.ValidatorAddr}"
        mtx = algosdk.encoding.future_msgpack_decode(self.HalfSignedCertCreationMtx)
        msig = mtx.multisig
        sender = msig.address()
        apar = mtx.transaction.dictify()["apar"]
        total = apar["t"]
        unit_name = apar["un"]
        manager = algosdk.encoding.encode_address(apar["m"])
        url = apar["au"]
        asset_name = apar["an"]
        r += "\n   HalfSignedCertCreationMtx - encoding of a half-signed mtx for this AssetCreationTransaction:"
        r += f"\n       sender=..{sender[-6:]}"
        r += f"\n       total={total}"
        r += "\n       decimals=0"
        r += f"\n       manager=..{manager[-6:]}"
        r += f"\n       asset_name={asset_name}"
        r += f"\n       unit_name={unit_name}"
        r += f"\n       url={url}"

        return r

    def axiom_1_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded HalfSignedCertCreationMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                f"Axiom 1: Decoded HalfSignedCertCreationMtx must have type MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def axiom_2_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 2: The HalfSignedCertCreationMtx.txn must have type transaction.AssetConfigTxn"""
        errors = []
        if not isinstance(txn, transaction.AssetConfigTxn):
            errors.append(
                f"Axiom 2: The HalfSignedCertCreationMtx.txn must have type transaction.AssetConfigTxn, got {type(txn)}"
            )
        return errors

    def axiom_3_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 2-sig Multi [Gnf Admin, payload.ValidatorAddr]"""
        errors = []
        msig = mtx.multisig
        gnf_admin_addr = config.Algo().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.ValidatorAddr],
        )
        if msig.address() != multi.addr:
            errors.append(
                f"Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 2-sig Multi [Gnf Admin, payload.ValidatorAddr].\nGot {msig.address()}.\nExpected {multi.addr}"
            )

        return errors

    def axiom_4_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 4: For the asset getting created: total = 1, unit_name=VLDTR, manager is Gnf Admin, asset_name and url not blank."""
        errors = []
        gnf_admin_addr = config.Algo().gnf_admin_addr
        od = txn.dictify()
        try:
            apar: OrderedDict = od["apar"]
        except:
            raise Exception(
                "Unexpected error. AssetCreationTxn.dictify() did not have 'apar' key"
            )
        if apar["t"] != 1:
            errors.append(f"notValidatorCertFormat - total must be 1, not {apar['t']}")
        if apar["un"] != "VLDTR":
            errors.append(
                f"notValidatorCertFormat - unit_name must be VLDTR, not {apar['un']}"
            )
        if apar["m"] != algosdk.encoding.decode_address(gnf_admin_addr):
            errors.append(
                f"notValidatorCertFormat - manager must be ..{gnf_admin_addr[-6:]}"
            )
        if "an" not in apar.keys():
            errors.append("asset-name must exist")
        if "au" not in apar.keys():
            errors.append("url must exist")
        return errors

    def axiom_5_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx"""
        errors = []
        try:
            api_utils.check_mtx_subsig(mtx, self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx: {e}"
            )
        return errors

    def axiom_6_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 6: There must not already be a ValidatorCert in the 2-sig
        [Gnf Admin, ValidatorAddr] acct."""
        errors = []
        existing_cert_idx = api_utils.get_validator_cert_idx(
            validator_addr=self.ValidatorAddr
        )
        if existing_cert_idx:
            errors.append(
                "There must not already be a ValidatorCert in the 2-sig [Gnf Admin, "
                f" ValidatorAddr] acct. Found {existing_cert_idx}"
            )
        return errors

    def axiom_errors(self):
        errors = []
        mtx = encoding.future_msgpack_decode(self.HalfSignedCertCreationMtx)
        errors += self.axiom_1_errors(mtx)
        if len(errors) != 0:
            return errors
        txn = mtx.transaction
        errors += self.axiom_2_errors(txn)
        if len(errors) != 0:
            return errors
        errors += self.axiom_3_errors(mtx=mtx)
        errors += self.axiom_4_errors(txn=txn)
        errors += self.axiom_5_errors(mtx=mtx)
        errors += self.axiom_6_errors(txn=txn)
        return errors
