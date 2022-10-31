"""create.tavalidatorcert.algo.010 type"""

import json
from typing import List
from typing import NamedTuple
from typing import OrderedDict

import algosdk
from algosdk import encoding
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
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
        except ValueError as e:
            errors.append(
                f"HalfSignedCertCreationMtx {self.HalfSignedCertCreationMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.ValidatorAddr, str):
            errors.append(f"ValidatorAddr {self.ValidatorAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.ValidatorAddr)
        except ValueError as e:
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

    def _axiom_1_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded HalfSignedCertCreationMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                f"Axiom 1: Decoded HalfSignedCertCreationMtx must have type MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def _axiom_2_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 2: The HalfSignedCertCreationMtx.txn must have type transaction.AssetConfigTxn"""
        errors = []
        if not isinstance(txn, transaction.AssetConfigTxn):
            errors.append(
                f"Axiom 2: The HalfSignedCertCreationMtx.txn must have type transaction.AssetConfigTxn, got {type(txn)}"
            )
        return errors

    def _axiom_3_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
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

    def _axiom_4_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
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

    def _axiom_5_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx"""
        errors = []
        try:
            api_utils.check_mtx_subsig(mtx, self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx: {e}"
            )
        return errors

    def _axiom_6_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
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
        errors += self._axiom_1_errors(mtx)
        if len(errors) != 0:
            return errors
        txn = mtx.transaction
        errors += self._axiom_2_errors(txn)
        if len(errors) != 0:
            return errors
        errors += self._axiom_3_errors(mtx=mtx)
        errors += self._axiom_4_errors(txn=txn)
        errors += self._axiom_5_errors(mtx=mtx)
        errors += self._axiom_6_errors(txn=txn)
        return errors


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
