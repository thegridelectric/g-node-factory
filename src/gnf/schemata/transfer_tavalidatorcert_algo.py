"""transfer.tavalidatorcert.algo.010 type"""

import json
from typing import List
from typing import NamedTuple
from typing import OrderedDict

import algosdk
from algosdk.future import transaction

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError


class TransferTavalidatorcertAlgo(NamedTuple):
    ValidatorAddr: str  #
    HalfSignedCertTransferMtx: str  #
    TypeName: str = "transfer.tavalidatorcert.algo.010"

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
        if not isinstance(self.HalfSignedCertTransferMtx, str):
            errors.append(
                f"HalfSignedCertTransferMtx {self.HalfSignedCertTransferMtx} must have type str."
            )
        try:
            property_format.check_is_algo_msg_pack_encoded(
                self.HalfSignedCertTransferMtx
            )
        except ValueError as e:
            errors.append(
                f"HalfSignedCertTransferMtx {self.HalfSignedCertTransferMtx}"
                " must have format AlgoMsgPackEncoded: {e}"
            )
        if self.TypeName != "transfer.tavalidatorcert.algo.010":
            errors.append(
                f"Type requires TypeName of transfer.tavalidatorcert.algo.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.axiom_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making transfer.tavalidatorcert.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferTavalidatorcertAlgo"

    def _axiom_1_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded HalfSignedCertTransferMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                "Axiom 1: Decoded HalfSignedCertTransferMtx must have type "
                f"MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def _axiom_2_errors(self, txn: transaction.AssetTransferTxn) -> List[str]:
        """Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn"""
        errors = []
        if not isinstance(txn, transaction.AssetTransferTxn):
            errors.append(
                "Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )
        return errors

    def _axiom_3_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 1-sig TaMulti
        [Gnf Admin, payload.ValidatorAddr]"""
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
                f"Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 1-sig TaMulti"
                "[Gnf Admin, payload.ValidatorAddr].\nGot {msig.address()}.\nExpected {multi.addr}"
            )

        return errors

    def _axiom_4_errors(self, txn: transaction.AssetTransferTxn):
        """Axiom 4: The Transfer asset-index must be for the existing Validator Certificate
        co-created by the multi account"""
        errors = []
        od: OrderedDict = txn.dictify()
        transfer_asset_idx = od["xaid"]
        validator_cert_idx = api_utils.get_validator_cert_idx(self.ValidatorAddr)
        if transfer_asset_idx != validator_cert_idx:
            errors.append(
                "Axiom 4: The Transfer asset-index must be for the existing Validator Certificate"
                "co-created by the multi account. Transfer request is for asset-index"
                f" {transfer_asset_idx} but the Validator Certificate idx is {validator_cert_idx}!"
            )
        return errors

    def _axiom_5_errors(self, txn: transaction.AssetTransferTxn):
        """Axiom 5: For the asset transfer: receiver is validator, sender is validator multi,
        transfer amount is 1"""
        errors = []
        od: OrderedDict = txn.dictify()
        validator_pk = algosdk.encoding.decode_address(self.ValidatorAddr)
        if od["arcv"] != validator_pk:
            errors.append(
                "Receiver should be ValidatorAddr (encoding.decode_address(ValidatorAddress)),"
                " not {od['arcv']} "
            )
        gnf_admin_addr = config.Algo().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.ValidatorAddr],
        )
        multi_pk = algosdk.encoding.decode_address(multi.addr)
        if od["snd"] != multi_pk:
            errors.append(
                f"Sender should be 2-sig [GnfAdmin, Validator] multi, not {od['snd']}"
            )

        # Check that the transfer request amount is 1
        if od["aamt"] != 1:
            errors.append(f"transfer request should be 1, not {od['aamt']} ")
        return errors

    def _axiom_6_errors(self, txn: transaction.AssetTransferTxn):
        """Axiom 6: Validator multi must have enough algos"""
        errors = []
        try:
            api_utils.check_validator_multi_has_enough_algos(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(e)
        return errors

    def _axiom_7_errors(self, txn: transaction.AssetTransferTxn):
        """Axiom 7: ValidatorAddr must have opted into the certificate, and the multi account must
        still own the certificate"""
        errors = []
        od: OrderedDict = txn.dictify()
        asset_index = od["xaid"]
        client = algo_utils.get_algod_client(config.Algo())
        validator_assets = client.account_info(self.ValidatorAddr)["assets"]
        if (
            len(list(filter(lambda x: x["asset-id"] == asset_index, validator_assets)))
            == 0
        ):
            errors.append(
                f"Axiom 7: ValidatorAddr {self.ValidatorAddr} has not opted in to certificate"
                f" {asset_index}"
            )
        gnf_admin_addr = config.Algo().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, self.ValidatorAddr],
        )
        multi_assets = client.account_info(multi.addr)["assets"]
        if len(list(filter(lambda x: x["asset-id"] == asset_index, multi_assets))) == 0:
            errors.append(
                f"Axiom 7:  multiasset  {multi.addr} never owned {asset_index}!"
            )
            return errors
        this_asset_dict: OrderedDict = list(
            filter(lambda x: x["asset-id"] == asset_index, multi_assets)
        )[0]
        if this_asset_dict["amount"] == 0:
            errors.append(
                f"Axiom 7:  multiasset  {multi.addr} no longer owns {asset_index}!"
            )
        return errors

    def _axiom_8_errors(self, mtx: transaction.MultisigTransaction):
        """Axiom 8: ValidatorAddr must have signed the mtx"""
        errors = []
        try:
            api_utils.check_mtx_subsig(mtx, self.ValidatorAddr)
        except SchemaError as e:
            errors.append(f"Axiom 5: ValidatorAddr must have signed the mtx: {e}")
        return errors

    def axiom_errors(self) -> List[str]:
        errors = []

        mtx = algosdk.encoding.future_msgpack_decode(self.HalfSignedCertTransferMtx)
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
        errors += self._axiom_7_errors(txn=txn)
        errors += self._axiom_8_errors(mtx=mtx)

        return errors


class TransferTavalidatorcertAlgo_Maker:
    type_name = "transfer.tavalidatorcert.algo.010"

    def __init__(self, validator_addr: str, half_signed_cert_transfer_mtx: str):

        gw_tuple = TransferTavalidatorcertAlgo(
            ValidatorAddr=validator_addr,
            HalfSignedCertTransferMtx=half_signed_cert_transfer_mtx,
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: TransferTavalidatorcertAlgo) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TransferTavalidatorcertAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TransferTavalidatorcertAlgo:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")
        if "ValidatorAddr" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing ValidatorAddr")
        if "HalfSignedCertTransferMtx" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing HalfSignedCertTransferMtx")

        gw_tuple = TransferTavalidatorcertAlgo(
            TypeName=new_d["TypeName"],
            ValidatorAddr=new_d["ValidatorAddr"],
            HalfSignedCertTransferMtx=new_d["HalfSignedCertTransferMtx"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
