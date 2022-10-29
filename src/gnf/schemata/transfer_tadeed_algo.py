"""transfer.tadeed.algo.010 type"""
from typing import List

import algo_utils
import api_utils
import config
from algo_utils import MultisigAccount
from algosdk import encoding
from algosdk.future.transaction import AssetTransferTxn
from algosdk.future.transaction import MultisigTransaction
from errors import SchemaError
from schemata.transfer_tadeed_algo_base import TransferTadeedAlgoBase


class TransferTadeedAlgo(TransferTadeedAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making exchange.tadeed.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferTadeedAlgo"

    def axiom_1_errors(self, mtx: MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, MultisigTransaction):
            errors.append(
                f"Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def axiom_2_errors(self, txn: AssetTransferTxn) -> List[str]:
        """Axiom 2: The FirstDeedTransferMtx.txn must have type AssetTransferTxn"""
        errors = []
        if not isinstance(txn, AssetTransferTxn):
            errors.append(
                "The FirstDeedTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )
        return errors

    def axiom_3_errors(self, mtx: MultisigTransaction) -> List[str]:
        """Axiom3: The MultiSig must belong to the 2-sig Multi [Gnf Admin, payload.DeedValidatorAddr]"""
        errors = []
        msig = mtx.multisig
        gnf_admin_addr = config.Algo().gnf_admin_addr
        multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.DeedValidatorAddr],
        )
        if msig.address() != multi.addr:
            errors.append(
                "Axiom 3: The MultiSig must belong to the 2-sig Multi "
                f"[Gnf Admin, payload.DeedValidatorAddr]. Got {msig.address()[-6:]}. Expected {multi.addr[-6:]}"
            )

        return errors

    def axiom_4_errors(self, txn: AssetTransferTxn) -> List[str]:
        """Axiom 4: The asset must be created and owned by the 2-sig
        [Gnf Admin, payload.DeedValidator] multi account"""
        errors = []
        client = algo_utils.get_algod_client(config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        v_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.DeedValidatorAddr],
        )
        ta_deed_idx = txn.dictify()["xaid"]
        try:
            created_assets = client.account_asset_info(
                address=v_multi.addr, asset_id=ta_deed_idx
            )
        except:
            errors.append(
                f"Axiom 4: The asset {ta_deed_idx} must be created and owned by the 2-sig "
                "[Gnf Admin, payload.DeedValidator] multi account. Not created"
            )
        if created_assets["asset-holding"]["amount"] == 0:
            errors.append(
                f"Axiom 4: The asset {ta_deed_idx} must be created and owned by the 2-sig "
                "[Gnf Admin, payload.DeedValidator] multi account. Created but not owned"
            )
        return errors

    def axiom_5_errors(self, txn: AssetTransferTxn) -> List[str]:
        """Axiom 5: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] account has opted in
        to the Deed and has enough funding (TaDeed Consideration Algos, publicly set by the Gnf)"""
        errors = []
        client = algo_utils.get_algod_client(config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.TaDaemonAddr, self.TaOwnerAddr],
        )
        ta_deed_idx = txn.dictify()["xaid"]
        try:
            client.account_asset_info(address=ta_multi.addr, asset_id=ta_deed_idx)
        except:
            errors.append(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must be opted in"
                f"to deed {ta_deed_idx}. It is not"
            )
        multi_algos = algo_utils.algos(ta_multi.addr)
        if multi_algos is None:
            errors.append(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must have at least"
                f"TaDeed Consideration Algos ({config.Algo().ta_deed_consideration_algos}). Has none"
            )
        elif multi_algos < config.Algo().ta_deed_consideration_algos:
            errors.append(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must have at least"
                f"TaDeed Consideration Algos ({config.Algo().ta_deed_consideration_algos}). Has none"
            )
        return errors

    def axiom_6_errors(self, txn: AssetTransferTxn) -> List[str]:
        """Axiom 6: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] must not own any assets
        (specifically because this is the FIRST tadeed and should initialize the multi."""
        errors = []
        client = algo_utils.get_algod_client(config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.TaDaemonAddr, self.TaOwnerAddr],
        )
        opt_in_assets = client.account_info(address=ta_multi.addr)["assets"]
        owned = list(
            map(
                lambda x: x["asset-id"],
                list(filter(lambda x: x["amount"] != 0, opt_in_assets)),
            )
        )
        if len(owned) > 0:
            errors.append(
                "Axiom 6: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] must not own"
                " any assets (specifically because this is the FIRST tadeed and should initialize"
                f"the multi. Owns: {owned}"
            )
        return errors

    def axiom_7_errors(self, mtx: MultisigTransaction) -> List[str]:
        """Axiom 7: The Mtx must be signed by the DeedValidatorAddr"""
        errors = []
        try:
            api_utils.check_mtx_subsig(mtx, self.DeedValidatorAddr)
        except SchemaError as e:
            errors.append(
                f"Axiom 5: The Mtx must be signed by the DeedValidatorAddr {e}"
            )
        return errors

    def axiom_errors(self) -> List[str]:
        errors = []
        mtx = encoding.future_msgpack_decode(self.FirstDeedTransferMtx)
        errors += self.axiom_1_errors(mtx)
        if len(errors) != 0:
            return errors
        txn = mtx.transaction
        errors += self.axiom_2_errors(txn)
        if len(errors) != 0:
            return errors
        errors += self.axiom_3_errors(mtx=mtx)
        errors += self.axiom_4_errors(txn=txn)
        errors += self.axiom_5_errors(txn=txn)
        errors += self.axiom_6_errors(txn=txn)
        errors += self.axiom_7_errors(mtx=mtx)
        return errors
