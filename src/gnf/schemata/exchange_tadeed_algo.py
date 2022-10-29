"""exchange.tadeed.algo.010 type"""
from typing import List

import algo_utils
import api_utils
import config
import property_format
from algo_utils import MultisigAccount
from algosdk import encoding
from algosdk.future import transaction
from errors import SchemaError
from schemata.exchange_tadeed_algo_base import ExchangeTadeedAlgoBase


class ExchangeTadeedAlgo(ExchangeTadeedAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        # errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making exchange.tadeed.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        r = "ExchangeTadeedAlgo"
        r += f"\n       TypeName: {self.TypeName}"
        r += f"\n       TaOwnerAddr: {self.TaOwnerAddr}"
        r += f"\n       TaDaemonAddr: {self.TaDaemonAddr}"
        r += f"\n       ValidatorAddr: {self.TaDaemonAddr}"
        r += f"\n       NewDeedIdx={self.NewTaDeedIdx}"
        mtx = encoding.future_msgpack_decode(self.OldDeedTransferMtx)
        msig = mtx.multisig
        sender = msig.address()
        od = mtx.transaction.dictify()
        total = od["aamt"]
        ta_deed_idx = od["xaid"]
        receiver = encoding.encode_address(od["arcv"])
        r += "\n       OldDeedTransferMtx - encoding of a half-signed mtx for transferring the old deed back to Gnf admin"
        r += f"\n         - sender=..{sender[-6:]}"
        r += f"\n         - total={total}"
        r += f"\n         - receiver=..{receiver[-6:]}"
        r += f"\n         - ta_deed_idx={ta_deed_idx}"
        return r

    def _axiom_4_errors(self) -> List[str]:
        """Axiom 4: OldDeedTransferMtx must be MultisigTransaction"""
        errors = []
        mtx = encoding.future_msgpack_decode(self.OldDeedTransferMtx)
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                f"Axiom 4: OldDeedTransferMtx must be MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def _axiom_5_errors(self) -> List[str]:
        """Axiom 5: OldDeedOptinMtx transaction must be an AssetTransferTxn"""
        errors = []
        txn = encoding.future_msgpack_decode(self.OldDeedTransferMtx).transaction
        if not isinstance(txn, transaction.AssetTransferTxn):
            errors.append(
                f"Axiom 5: OldDeedOptinMtx transaction must be an AssetTransferTxn, got {type(txn)}"
            )
        return errors

    def _axiom_6_errors(self) -> List[str]:
        """Axiom 6 (Txn consistency check). Total must be 1, sender must be ta_multi, receiver
        must be GnfAdmin, asset must be a TaDeed"""
        errors = []
        txn = encoding.future_msgpack_decode(self.OldDeedTransferMtx).transaction
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        gnf_admin_addr = config.Algo().gnf_admin_addr
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.TaDaemonAddr, self.TaOwnerAddr],
        )
        v_multi = MultisigAccount(
            version=1, threshold=2, addresses=[gnf_admin_addr, self.ValidatorAddr]
        )
        if txn.sender != ta_multi.addr:
            errors.append(
                f"Axiom 3: Sender address ..{txn.sender[-6:]} must be ta_multi addr ..{ta_multi.addr[-6:]}"
            )
        od = txn.dictify()
        if txn.receiver != gnf_admin_addr:
            errors.append(
                f"Axiom 3: Receiver address ..{txn.receiver[-6:]} must be Gnf Adminaddr ..{gnf_admin_addr[-6:]}"
            )
        if txn.amount != 1:
            errors.append(f"Axiom 3: Transfer total must be 1, not {txn.amount}")
        ta_deed_idx = txn.index
        client = algo_utils.get_algod_client(settings_algo=config.Algo())
        asset_dict = client.asset_info(ta_deed_idx)["params"]
        if (
            asset_dict["unit-name"] != "TADEED"
            or asset_dict["total"] != 1
            or asset_dict["manager"] != gnf_admin_addr
        ):
            errors.append(
                "Axiom 6 (Txn consistency check): asset must be a valid TaDeed!"
            )

        old_ta_deed_g_node_alias = asset_dict["name"]
        try:
            property_format.check_is_lrd_alias_format(old_ta_deed_g_node_alias)
        except SchemaError as e:
            errors.append(f"The asset name must have valid GNode format: {e}")
        universe = config.Algo().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=old_ta_deed_g_node_alias, universe=universe
            )
        except:
            errors.append(
                f"The asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )

        creator_addr = asset_dict["creator"]
        if creator_addr not in [v_multi.addr, gnf_admin_addr]:
            errors.append(
                f"Axiom 3: Creator must be Gnf Admin ..{gnf_admin_addr[-6:]} or "
                f"Validator Multi ..{v_multi.addr[-6:]}. Got {creator_addr[-6:]}"
            )

        gnf_graveyard_addr = config.Algo().gnf_graveyard_addr
        manager_addr = asset_dict["manager"]
        if manager_addr not in [gnf_admin_addr, gnf_graveyard_addr]:
            errors.append(
                f"Axiom 3: Manager must be GnfAdmin ..{gnf_admin_addr[-6:]} or "
                f"GnfGraveyard ..{gnf_graveyard_addr[-6:]}. Got {manager_addr[-6:]}"
            )

        return errors

    def _axiom_7_errors(self) -> List[str]:
        """Axiom 7 (TaDeed order): The asset index of the new deed must be greater than the
        asset index of the old deed"""
        errors = []
        txn = encoding.future_msgpack_decode(self.OldDeedTransferMtx).transaction
        old_ta_deed_idx = txn.index
        if old_ta_deed_idx > self.NewTaDeedIdx:
            errors.append(
                "Axiom 7 (TaDeed order):The asset index of the new deed must be greater than"
                " the asset index of the old deed "
            )
        return errors

    def _axiom_8_errors(self) -> List[str]:
        """Axiom 8 (Correctly signed): OldDeedTransferMtx must be signed by Gnf Admin, and the
        signature must match the txn."""
        errors = []
        mtx = encoding.future_msgpack_decode(self.OldDeedTransferMtx)
        gnf_admin_addr = config.Algo().gnf_admin_addr
        try:
            api_utils.check_mtx_subsig(mtx, gnf_admin_addr)
        except SchemaError as e:
            errors.append(f"OldDeedTransferMtx must be signed by Gnf Admin: {e}")
        # TODO: check that the signature matches the txn
        return errors

    def axiom_errors(self) -> List[str]:
        errors = []
        errors += self._axiom_4_errors()
        if len(errors) != 0:
            return errors
        errors += self._axiom_5_errors()
        if len(errors) != 0:
            return errors
        errors += self._axiom_6_errors()
        errors += self._axiom_7_errors()
        errors += self._axiom_8_errors()
        return errors
