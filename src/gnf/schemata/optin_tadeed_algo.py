"""optin.tadeed.algo.001 type"""
from typing import List

import algo_utils
import api_utils
import config
import property_format
from algosdk import encoding
from algosdk.future import transaction
from errors import SchemaError
from schemata.optin_tadeed_algo_base import OptinTadeedAlgoBase


class OptinTadeedAlgo(OptinTadeedAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making optin.tadeed.algo.001 for {self}: {errors}"
            )

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
