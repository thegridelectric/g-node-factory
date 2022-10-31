"""optin.tadeed.algo.001 type"""

import json
from typing import List
from typing import NamedTuple

from algosdk import encoding
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError


class OptinTadeedAlgo(NamedTuple):
    ValidatorAddr: str  #
    NewDeedOptInMtx: str  #
    TaOwnerAddr: str  #
    TaDaemonAddr: str  #
    TypeName: str = "optin.tadeed.algo.001"

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
                f"Errors making optin.tadeed.algo.001 for {self}: {errors}"
            )

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
        if not isinstance(self.NewDeedOptInMtx, str):
            errors.append(f"NewDeedOptInMtx {self.NewDeedOptInMtx} must have type str.")
        try:
            property_format.check_is_algo_msg_pack_encoded(self.NewDeedOptInMtx)
        except ValueError as e:
            errors.append(
                f"NewDeedOptInMtx {self.NewDeedOptInMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except ValueError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.TaDaemonAddr, str):
            errors.append(f"TaDaemonAddr {self.TaDaemonAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaDaemonAddr)
        except ValueError as e:
            errors.append(
                f"TaDaemonAddr {self.TaDaemonAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if self.TypeName != "optin.tadeed.algo.001":
            errors.append(
                f"Type requires TypeName of optin.tadeed.algo.001, not {self.TypeName}."
            )

        return errors

    def __repr__(self):
        return "OptinTadeedAlgo"

    def _axiom_4_errors(self) -> List[str]:
        """Axiom 4 (NewDeedOptInMtx is MultisigTransaction): Once decoded, NewDeedOptInMtx is
        a MultisigTransaction"""
        errors = []
        mtx = encoding.future_msgpack_decode(self.NewDeedOptInMtx)
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                "Axiom 4 (NewDeedOptInMtx is MultisigTransaction): Once decoded, NewDeedOptInMtx"
                f"is a MultisigTransaction. Got {type(mtx)}"
            )
        return errors

    def _axiom_5_errors(self) -> List[str]:
        """Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an OptIn
        Transaction"""
        errors = []
        txn = encoding.future_msgpack_decode(self.NewDeedOptInMtx).transaction
        if not isinstance(txn, transaction.AssetTransferTxn):
            errors.append(
                "Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an"
                f" OptIn Transaction. Got {type(txn)}"
            )
        if txn.sender != txn.receiver:
            errors.append(
                "Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an"
                " OptIn Transaction. But txn.sender != txn.receiver!"
            )
        if txn.amount != 0:
            errors.append(
                "Axiom 5 (NewDeedOptinMtx txn type check): NewDeedOptinMtx transaction must be an"
                f" OptIn Transaction. But txn.amount != 0 ({txn.amount})"
            )
        return errors

    def _axiom_6_errors(self) -> List[str]:
        """Axiom 6 (Txn consistency check): Txn sender is TaMulti, OptIn asset is an active
        TaDeed created and owned by GnfAdminAccount"""
        errors = []
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        txn = encoding.future_msgpack_decode(self.NewDeedOptInMtx).transaction
        ta_multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.TaDaemonAddr, self.TaOwnerAddr],
        )
        if txn.sender != ta_multi.addr:
            errors.append(
                "Axiom 6 (Txn consistency check): Txn sender must be TaMulti. But"
                f" Txn sender is ..{txn.sender[-6:]} and TaMulti is ..{ta_multi.addr[-6:]}"
            )

        new_ta_deed_idx = txn.index
        try:
            gnf_new_deed_info = client.account_asset_info(
                address=gnf_admin_addr, asset_id=new_ta_deed_idx
            )
        except:
            errors.append(
                "Axiom 6 (Txn consistency check): OptIn asset must be created by GnfAdminAccount!"
            )
        if (
            gnf_new_deed_info["created-asset"]["unit-name"] != "TADEED"
            or gnf_new_deed_info["created-asset"]["total"] != 1
            or gnf_new_deed_info["created-asset"]["manager"] != gnf_admin_addr
        ):
            errors.append(
                "Axiom 6 (Txn consistency check): Optin asset must be a valid TaDeed!"
            )
        ta_deed_g_node_alias = gnf_new_deed_info["created-asset"]["name"]
        try:
            property_format.check_is_lrd_alias_format(ta_deed_g_node_alias)
        except SchemaError as e:
            errors.append(f"Axiom 6: Optin asset must be a valid TaDeed! {e}")
        universe = config.Algo().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=ta_deed_g_node_alias, universe=universe
            )
        except:
            errors.append(
                f"Axiom 6. The asset not a valid TaDeed! asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )
        if gnf_new_deed_info["asset-holding"]["amount"] != 1:
            errors.append(
                "Axiom 6 (Txn consistency check): Optin asset must be owned by GnfAdminAccount!"
            )
        return errors

    def _axiom_7_errors(self) -> List[str]:
        """Axiom 7 (Old TaDeed and Validator check): TaMulti 2-sig [GnfAdminAccount, TaDaemonAddr,
        TaOwnerAddr] owns exactly 1 TaDeed. The creator of the old TaDeed is either the GnfAdminAccount
        or the ValidatorMulti 2-sig [GnfAdminAccount, ValidatorAddr]. The asset index of the old TaDeed is
        less than the asset index of the new TaDeed. Finally, if the creator of the old TaDeed is the
        GnfAdminAccount, then the TaMulti is opted into (but does not own) exactly one TaDeed created by the
        ValidatorMulti account and owned by the GnfAdminAccount"""
        errors = []
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        txn = encoding.future_msgpack_decode(self.NewDeedOptInMtx).transaction
        ta_multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.TaDaemonAddr, self.TaOwnerAddr],
        )
        new_ta_deed_idx = txn.index
        # TODO: implement!!

        return errors

    def _axiom_8_errors(self) -> List[str]:
        """Axiom 8 (Correctly Signed) NewDeedOptInMtx must be signed by Gnf Admin, and the signature
        must match the txn."""
        errors = []
        mtx = encoding.future_msgpack_decode(self.NewDeedOptInMtx)
        gnf_admin_addr = config.Algo().gnf_admin_addr
        try:
            api_utils.check_mtx_subsig(mtx, gnf_admin_addr)
        except SchemaError as e:
            errors.append(
                f"Axiom 8 (Correctly Signed): NewDeedOptInMtx must be signed by Gnf Admin: {e}"
            )
        # TODO: check that the signature matches the txn
        return errors

    def axiom_errors(self):
        errors = []
        errors += self._axiom_4_errors()
        if len(errors) != 0:
            return errors
        errors += self._axiom_5_errors()
        if len(errors) != 0:
            return errors
        errors += self._axiom_6_errors()
        if errors != []:
            return errors
        errors += self._axiom_7_errors()
        errors += self._axiom_8_errors()
        return errors


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo.001"

    def __init__(
        self,
        validator_addr: str,
        new_deed_opt_in_mtx: str,
        ta_owner_addr: str,
        ta_daemon_addr: str,
    ):

        gw_tuple = OptinTadeedAlgo(
            ValidatorAddr=validator_addr,
            NewDeedOptInMtx=new_deed_opt_in_mtx,
            TaOwnerAddr=ta_owner_addr,
            TaDaemonAddr=ta_daemon_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: OptinTadeedAlgo) -> str:
        tuple.check_for_errors()
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
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "NewDeedOptInMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing NewDeedOptInMtx")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")

        gw_tuple = OptinTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            NewDeedOptInMtx=new_d["NewDeedOptInMtx"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
