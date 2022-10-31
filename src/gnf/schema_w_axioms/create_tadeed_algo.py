"""create.tadeed.algo.010 type"""

import json
from typing import List
from typing import NamedTuple
from typing import OrderedDict

from algosdk import encoding
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
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
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.tavalidatorcert.algo.010: {errors}"
            )

    def __repr__(self):
        r = "CreateTadeedAlgo"
        r += f"\n   API TypeName: {self.TypeName}"
        r += f"\n   ValidatorAddr: {self.ValidatorAddr}"
        mtx = encoding.future_msgpack_decode(self.HalfSignedDeedCreationMtx)
        msig = mtx.multisig
        sender = msig.address()
        apar = mtx.transaction.dictify()["apar"]
        total = apar["t"]
        unit_name = apar["un"]
        manager = encoding.encode_address(apar["m"])
        asset_name = apar["an"]
        r += "\n   HalfSignedDeedCreationMtx - encoding of a half-signed mtx for this AssetCreationTransaction:"
        r += f"\n       sender=..{sender[-6:]}"
        r += f"\n       total={total}"
        r += "\n       decimals=0"
        r += f"\n       manager=..{manager[-6:]}"
        r += f"\n       asset_name={asset_name}"
        r += f"\n       unit_name={unit_name}"

        return r

    def _axiom_1_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                "Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        return errors

    def _axiom_2_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn"""
        errors = []
        if not isinstance(txn, transaction.AssetConfigTxn):
            errors.append(
                f"Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn, got {type(txn)}"
            )
        return errors

    def _axiom_3_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 3: The MultiSig must be the 2-sig multi [Gnf Admin, payload.ValidatorAddr]"""
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
                "Axiom 3: The MultiSig must be the 2-sig multi"
                f"[Gnf Admin, payload.ValidatorAddr].\nGot ..{msig.address()[-6:]}.\nExpected ..{multi.addr[-6:]}"
            )

        return errors

    def _axiom_4_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """Axiom 4: For the asset getting created: total = 1, unit_name=TADEED, asset_name
        must be <= 32 char, manager is Gnf Admin."""
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
            errors.append(f"total must be 1, not {apar['t']}. ")
        if apar["un"] != "TADEED":
            errors.append(
                f"not a TaDeed - unit_name must be TADEED, not {apar['un']}. "
            )
        if apar["m"] != encoding.decode_address(gnf_admin_addr):
            errors.append(
                f"Manager must be GnfAdmin ..{gnf_admin_addr[-6:]}, got ..{encoding.encode_address(apar['m'])[-6:]}. "
            )
        if len(apar["an"]) > 32:
            errors.append(f"asset name must be <= 32 char. Got {len(apar['an'])} ")
        return errors

    def _axiom_5_errors(self, txn: transaction.AssetCreateTxn) -> List[str]:
        """The asset name must have valid GNodeAlias format, with the world_alias (first
        word of asset name matching the universe (e.g. dev universe -> world starts with `d`).
        Additionally, the final word of the asset name must be `ta`"""
        errors = []
        asset_name = txn.dictify()["apar"]["an"]

        try:
            property_format.check_is_lrd_alias_format(asset_name)
        except SchemaError as e:
            errors.append(f"The asset name must have valid GNode format: {e}")
        universe = config.Algo().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=asset_name, universe=universe
            )
        except SchemaError as e:
            errors.append(
                f"The asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )
        words = asset_name.split(".")
        if words[-1] != "ta":
            errors.append(f"TerminalAsset aliases must end in ta. Got {asset_name}")
        return errors

    def _axiom_6_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 6: ValidatorAddr must have signed the mtx, and the signature must match the txn"""
        errors = []
        try:
            api_utils.check_mtx_subsig(mtx, self.ValidatorAddr)
        except SchemaError as e:
            errors.append(
                "Axiom 5: ValidatorAddr must have signed the mtx, and the signature must"
                f" match the txn: {e}"
            )
        return errors

    def axiom_errors(self):
        errors = []
        mtx = encoding.future_msgpack_decode(self.HalfSignedDeedCreationMtx)
        errors += self._axiom_1_errors(mtx)
        if len(errors) != 0:
            return errors
        txn = mtx.transaction
        errors += self._axiom_2_errors(txn)
        if len(errors) != 0:
            return errors
        errors += self._axiom_3_errors(mtx=mtx)
        errors += self._axiom_4_errors(txn=txn)
        errors += self._axiom_5_errors(txn=txn)
        errors += self._axiom_6_errors(mtx=mtx)
        return errors


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
