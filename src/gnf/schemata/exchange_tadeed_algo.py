"""exchange.tadeed.algo.010 type"""

import json
from typing import List
from typing import NamedTuple

from algosdk import encoding
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.algo_utils import MultisigAccount
from gnf.errors import SchemaError


class ExchangeTadeedAlgo(NamedTuple):
    ValidatorAddr: str  #
    TaOwnerAddr: str  #
    NewTaDeedIdx: int  #
    OldDeedTransferMtx: str  #
    TaDaemonAddr: str  #
    TypeName: str = "exchange.tadeed.algo.010"

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
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except ValueError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.NewTaDeedIdx, int):
            errors.append(f"NewTaDeedIdx {self.NewTaDeedIdx} must have type int.")
        if not isinstance(self.OldDeedTransferMtx, str):
            errors.append(
                f"OldDeedTransferMtx {self.OldDeedTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(self.OldDeedTransferMtx)
        except ValueError as e:
            errors.append(
                f"OldDeedTransferMtx {self.OldDeedTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
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
        if self.TypeName != "exchange.tadeed.algo.010":
            errors.append(
                f"Type requires TypeName of exchange.tadeed.algo.010, not {self.TypeName}."
            )

        return errors

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


class ExchangeTadeedAlgo_Maker:
    type_name = "exchange.tadeed.algo.010"

    def __init__(
        self,
        validator_addr: str,
        ta_owner_addr: str,
        new_ta_deed_idx: int,
        old_deed_transfer_mtx: str,
        ta_daemon_addr: str,
    ):

        gw_tuple = ExchangeTadeedAlgo(
            ValidatorAddr=validator_addr,
            TaOwnerAddr=ta_owner_addr,
            NewTaDeedIdx=new_ta_deed_idx,
            OldDeedTransferMtx=old_deed_transfer_mtx,
            TaDaemonAddr=ta_daemon_addr,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: ExchangeTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> ExchangeTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> ExchangeTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "NewTaDeedIdx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing NewTaDeedIdx")
        if "OldDeedTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing OldDeedTransferMtx")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")

        gw_tuple = ExchangeTadeedAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            NewTaDeedIdx=new_d["NewTaDeedIdx"],
            OldDeedTransferMtx=new_d["OldDeedTransferMtx"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
