"""Type tadeed.algo.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal
from typing import OrderedDict

from algosdk import encoding
from algosdk.future import transaction
from pydantic import BaseModel
from pydantic import root_validator

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedAlgoCreate(BaseModel):
    ValidatorAddr: str  #
    HalfSignedDeedCreationMtx: str  #
    TypeName: Literal["tadeed.algo.create"] = "tadeed.algo.create"
    Version: str = "000"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_deed_creation_mtx = predicate_validator(
        "HalfSignedDeedCreationMtx", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axioms_1_and_2(cls, v) -> Any:
        """Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction.
        Axiom 2:  The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedDeedCreationMtx", None))
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        txn = mtx.transaction
        if not isinstance(txn, transaction.AssetConfigTxn):
            raise ValueError(
                f"Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn, got {type(txn)}"
            )
        return v

    @root_validator
    def _axiom_3(cls, v) -> Any:
        """Axiom 3: The MultiSig must be the 2-sig multi [Gnf Admin, payload.ValidatorAddr]"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedDeedCreationMtx", None))
        ValidatorAddr = v.get("ValidatorAddr", None)
        msig = mtx.multisig
        gnf_admin_addr = config.Algo().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, ValidatorAddr],
        )
        if msig.address() != multi.addr:
            raise ValueError(
                "Axiom 3: The MultiSig must be the 2-sig multi"
                f"[Gnf Admin, payload.ValidatorAddr].\nGot ..{msig.address()[-6:]}.\nExpected ..{multi.addr[-6:]}"
            )

        return v

    @root_validator
    def _axiom_4(cls, v) -> Any:
        """Axiom 4: For the asset getting created: total = 1, unit_name=TADEED, asset_name
        must be <= 32 char, manager is Gnf Admin."""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedDeedCreationMtx", None))
        txn = mtx.transaction
        gnf_admin_addr = config.Algo().gnf_admin_addr
        od = txn.dictify()
        try:
            apar: OrderedDict = od["apar"]
        except:
            raise Exception(
                "Unexpected error. AssetCreationTxn.dictify() did not have 'apar' key"
            )
        if apar["t"] != 1:
            raise ValueError(f"total must be 1, not {apar['t']}. ")
        if apar["un"] != "TADEED":
            raise ValueError(
                f"Axiom 4: not a TaDeed - unit_name must be TADEED, not {apar['un']}. "
            )
        if apar["m"] != encoding.decode_address(gnf_admin_addr):
            raise ValueError(
                f"Manager must be GnfAdmin ..{gnf_admin_addr[-6:]}, got ..{encoding.encode_address(apar['m'])[-6:]}. "
            )
        if len(apar["an"]) > 32:
            raise ValueError(f"asset name must be <= 32 char. Got {len(apar['an'])} ")

        return v

    @root_validator
    def _axiom_5(cls, v) -> Any:
        """The asset name must have valid GNodeAlias format, with the world_alias (first
        word of asset name matching the universe (e.g. dev universe -> world starts with `d`).
        Additionally, the final word of the asset name must be `ta`"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedDeedCreationMtx", None))
        txn = mtx.transaction

        asset_name = txn.dictify()["apar"]["an"]

        try:
            property_format.check_is_lrd_alias_format(asset_name)
        except SchemaError as e:
            raise ValueError(f"The asset name must have valid GNode format: {e}")
        universe = config.Algo().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=asset_name, universe=universe
            )
        except SchemaError as e:
            raise ValueError(
                f"The asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )
        words = asset_name.split(".")
        if words[-1] != "ta":
            raise ValueError(f"TerminalAsset aliases must end in ta. Got {asset_name}")

        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6: ValidatorAddr must have signed the mtx, and the signature must match the txn"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedDeedCreationMtx", None))
        ValidatorAddr = v.get("ValidatorAddr")
        try:
            api_utils.check_mtx_subsig(mtx, ValidatorAddr)
        except SchemaError as e:
            raise ValueError(
                "Axiom 5: ValidatorAddr must have signed the mtx, and the signature must"
                f" match the txn: {e}"
            )

        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

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


class TadeedAlgoCreate_Maker:
    type_name = "tadeed.algo.create"
    version = "000"

    def __init__(self, validator_addr: str, half_signed_deed_creation_mtx: str):

        self.tuple = TadeedAlgoCreate(
            ValidatorAddr=validator_addr,
            HalfSignedDeedCreationMtx=half_signed_deed_creation_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedAlgoCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedAlgoCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TadeedAlgoCreate:
        d2 = dict(d)
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "HalfSignedDeedCreationMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HalfSignedDeedCreationMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedAlgoCreate(
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedDeedCreationMtx=d2["HalfSignedDeedCreationMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
