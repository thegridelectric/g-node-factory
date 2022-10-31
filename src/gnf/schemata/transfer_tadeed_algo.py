"""transfer.tadeed.algo.020 type"""

import json
from typing import List
from typing import NamedTuple

from algosdk import encoding
from algosdk.future.transaction import AssetTransferTxn
from algosdk.future.transaction import MultisigTransaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.algo_utils import MultisigAccount
from gnf.errors import SchemaError


class TransferTadeedAlgo(NamedTuple):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: str = "transfer.tadeed.algo.020"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.FirstDeedTransferMtx, str):
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(self.FirstDeedTransferMtx)
        except ValueError as e:
            errors.append(
                f"FirstDeedTransferMtx {self.FirstDeedTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if not isinstance(self.MicroLat, int):
            errors.append(f"MicroLat {self.MicroLat} must have type int.")
        if not isinstance(self.DeedValidatorAddr, str):
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr} must have type str."
            )
        try:
            property_format.check_is_algo_address_string_format(self.DeedValidatorAddr)
        except ValueError as e:
            errors.append(
                f"DeedValidatorAddr {self.DeedValidatorAddr}"
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
        if not isinstance(self.TaOwnerAddr, str):
            errors.append(f"TaOwnerAddr {self.TaOwnerAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.TaOwnerAddr)
        except ValueError as e:
            errors.append(
                f"TaOwnerAddr {self.TaOwnerAddr}"
                " must have format AlgoAddressStringFormat: {e}"
            )
        if not isinstance(self.MicroLon, int):
            errors.append(f"MicroLon {self.MicroLon} must have type int.")
        if self.TypeName != "transfer.tadeed.algo.020":
            errors.append(
                f"Type requires TypeName of transfer.tadeed.algo.020, not {self.TypeName}."
            )

        return errors

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

    def _axiom_1_errors(self, mtx: MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, MultisigTransaction):
            errors.append(
                f"Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def _axiom_2_errors(self, txn: AssetTransferTxn) -> List[str]:
        """Axiom 2: The FirstDeedTransferMtx.txn must have type AssetTransferTxn"""
        errors = []
        if not isinstance(txn, AssetTransferTxn):
            errors.append(
                "The FirstDeedTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )
        return errors

    def _axiom_3_errors(self, mtx: MultisigTransaction) -> List[str]:
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

    def _axiom_4_errors(self, txn: AssetTransferTxn) -> List[str]:
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

    def _axiom_5_errors(self, txn: AssetTransferTxn) -> List[str]:
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

    def _axiom_6_errors(self, txn: AssetTransferTxn) -> List[str]:
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

    def _axiom_7_errors(self, mtx: MultisigTransaction) -> List[str]:
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
        errors += self._axiom_6_errors(txn=txn)
        errors += self._axiom_7_errors(mtx=mtx)
        return errors


class TransferTadeedAlgo_Maker:
    type_name = "transfer.tadeed.algo.020"

    def __init__(
        self,
        first_deed_transfer_mtx: str,
        micro_lat: int,
        deed_validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lon: int,
    ):

        gw_tuple = TransferTadeedAlgo(
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            MicroLat=micro_lat,
            DeedValidatorAddr=deed_validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLon=micro_lon,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: TransferTadeedAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferTadeedAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "FirstDeedTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing FirstDeedTransferMtx")
        if "MicroLat" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLat")
        if "DeedValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing DeedValidatorAddr")
        if "TaDaemonAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaDaemonAddr")
        if "TaOwnerAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TaOwnerAddr")
        if "MicroLon" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing MicroLon")

        gw_tuple = TransferTadeedAlgo(
            TypeName=new_d["TypeName"],
            FirstDeedTransferMtx=new_d["FirstDeedTransferMtx"],
            MicroLat=new_d["MicroLat"],
            DeedValidatorAddr=new_d["DeedValidatorAddr"],
            TaDaemonAddr=new_d["TaDaemonAddr"],
            TaOwnerAddr=new_d["TaOwnerAddr"],
            MicroLon=new_d["MicroLon"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
