"""Type optin.tadeed.algo, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import NamedTuple

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


class OptinTadeedAlgo(BaseModel):
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TypeName: Literal["optin.tadeed.algo"] = "optin.tadeed.algo"
    Version: str = "000"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_new_deed_opt_in_mtx = predicate_validator(
        "NewDeedOptInMtx", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axioms_4_and_5(cls, v) -> Any:
        """Axiom 4:(NewDeedOptInMtx is MultisigTransaction): Once decoded, NewDeedOptInMtx is
        a MultisigTransaction
        Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an OptIn
        Transaction"""
        mtx = encoding.future_msgpack_decode(v.get("NewDeedOptInMtx", None))
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 4: Decoded NewDeedOptInMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        txn = mtx.transaction
        if not isinstance(txn, transaction.AssetTransferTxn):
            raise ValueError(
                f"Axiom 5: The NewDeedOptInMtx.txn must have type AssetTransferTxn, got {type(txn)}"
            )
        if txn.sender != txn.receiver:
            raise ValueError(
                "Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an"
                " OptIn Transaction. But txn.sender != txn.receiver!"
            )
        if txn.amount != 0:
            raise ValueError(
                "Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an"
                f" OptIn Transaction. But txn.amount != 0 ({txn.amount})"
            )

        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6 (Txn consistency check): Txn sender is TaMulti, OptIn asset is an active
        TaDeed created and owned by GnfAdminAccount"""
        errors = []
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        mtx = encoding.future_msgpack_decode(v.get("NewDeedOptInMtx", None))
        txn = mtx.transaction
        TaDaemonAddr = v.get("TaDaemonAddr")
        TaOwnerAddr = v.get("TaOwnerAddr")
        ta_multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, TaDaemonAddr, TaOwnerAddr],
        )
        if txn.sender != ta_multi.addr:
            raise ValueError(
                "Axiom 6 (Txn consistency check): Txn sender must be TaMulti. But"
                f" Txn sender is ..{txn.sender[-6:]} and TaMulti is ..{ta_multi.addr[-6:]}"
            )

        new_ta_deed_idx = txn.index
        try:
            gnf_new_deed_info = client.account_asset_info(
                address=gnf_admin_addr, asset_id=new_ta_deed_idx
            )
        except:
            raise ValueError(
                "Axiom 6 (Txn consistency check): OptIn asset must be created by GnfAdminAccount!"
            )
        if (
            gnf_new_deed_info["created-asset"]["unit-name"] != "TADEED"
            or gnf_new_deed_info["created-asset"]["total"] != 1
            or gnf_new_deed_info["created-asset"]["manager"] != gnf_admin_addr
        ):
            raise ValueError(
                "Axiom 6 (Txn consistency check): Optin asset must be a valid TaDeed!"
            )
        ta_deed_g_node_alias = gnf_new_deed_info["created-asset"]["name"]
        try:
            property_format.check_is_lrd_alias_format(ta_deed_g_node_alias)
        except SchemaError as e:
            raise ValueError(f"Axiom 6: Optin asset must be a valid TaDeed! {e}")
        universe = config.Algo().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=ta_deed_g_node_alias, universe=universe
            )
        except:
            raise ValueError(
                f"Axiom 6. The asset not a valid TaDeed! asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )
        if gnf_new_deed_info["asset-holding"]["amount"] != 1:
            raise ValueError(
                "Axiom 6 (Txn consistency check): Optin asset must be owned by GnfAdminAccount!"
            )

        return v

    @root_validator
    def _axiom_7(cls, v: Dict | Any) -> Any:
        """Axiom 7 (Old TaDeed and Validator check): TaMulti 2-sig [GnfAdminAccount, TaDaemonAddr,
        TaOwnerAddr] owns exactly 1 TaDeed. The creator of the old TaDeed is either the GnfAdminAccount
        or the ValidatorMulti 2-sig [GnfAdminAccount, ValidatorAddr]. The asset index of the old TaDeed is
        less than the asset index of the new TaDeed. Finally, if the creator of the old TaDeed is the
        GnfAdminAccount, then the TaMulti is opted into (but does not own) exactly one TaDeed created by the
        ValidatorMulti account and owned by the GnfAdminAccount"""
        mtx = encoding.future_msgpack_decode(v.get("NewDeedOptInMtx", None))
        txn = mtx.transaction
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        TaDaemonAddr = v.get("TaDaemonAddr")
        TaOwnerAddr = v.get("TaOwnerAddr")
        ta_multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, TaDaemonAddr, TaOwnerAddr],
        )
        new_ta_deed_idx = txn.index
        # TODO: implement!!

        return v

    @root_validator
    def _axiom_8(cls, v) -> Any:
        """Axiom 8 (Correctly Signed) NewDeedOptInMtx must be signed by Gnf Admin, and the signature
        must match the txn."""
        mtx = encoding.future_msgpack_decode(v.get("NewDeedOptInMtx", None))
        gnf_admin_addr = config.Algo().gnf_admin_addr
        try:
            api_utils.check_mtx_subsig(mtx, gnf_admin_addr)
        except SchemaError as e:
            raise ValueError(
                f"Axiom 8 (Correctly Signed): NewDeedOptInMtx must be signed by Gnf Admin: {e}"
            )
        # TODO: check that the signature matches the txn
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo"
    version = "000"

    def __init__(
        self,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        validator_addr: str,
        new_deed_opt_in_mtx: str,
    ):

        self.tuple = OptinTadeedAlgo(
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            ValidatorAddr=validator_addr,
            NewDeedOptInMtx=new_deed_opt_in_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: OptinTadeedAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> OptinTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> OptinTadeedAlgo:
        d2 = dict(d)
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "NewDeedOptInMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NewDeedOptInMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return OptinTadeedAlgo(
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            NewDeedOptInMtx=d2["NewDeedOptInMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
