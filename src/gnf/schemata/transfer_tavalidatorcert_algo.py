"""transfer.tavalidatorcert.algo.010 type"""
from typing import List
from typing import OrderedDict

import algo_utils
import algosdk
import api_utils
import config
from algosdk.future import transaction
from errors import SchemaError
from schemata.transfer_tavalidatorcert_algo_base import TransferTavalidatorcertAlgoBase


class TransferTavalidatorcertAlgo(TransferTavalidatorcertAlgoBase):
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

    def axiom_1_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
        """Axiom 1: Decoded HalfSignedCertTransferMtx must have type MultisigTransaction"""
        errors = []
        if not isinstance(mtx, transaction.MultisigTransaction):
            errors.append(
                "Axiom 1: Decoded HalfSignedCertTransferMtx must have type "
                f"MultisigTransaction, got {type(mtx)}"
            )
        return errors

    def axiom_2_errors(self, txn: transaction.AssetTransferTxn) -> List[str]:
        """Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn"""
        errors = []
        if not isinstance(txn, transaction.AssetTransferTxn):
            errors.append(
                "Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )
        return errors

    def axiom_3_errors(self, mtx: transaction.MultisigTransaction) -> List[str]:
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

    def axiom_4_errors(self, txn: transaction.AssetTransferTxn):
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

    def axiom_5_errors(self, txn: transaction.AssetTransferTxn):
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

    def axiom_6_errors(self, txn: transaction.AssetTransferTxn):
        """Axiom 6: Validator multi must have enough algos"""
        errors = []
        try:
            api_utils.check_validator_multi_has_enough_algos(self.ValidatorAddr)
        except SchemaError as e:
            errors.append(e)
        return errors

    def axiom_7_errors(self, txn: transaction.AssetTransferTxn):
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

    def axiom_8_errors(self, mtx: transaction.MultisigTransaction):
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
        errors += self.axiom_7_errors(txn=txn)
        errors += self.axiom_8_errors(mtx=mtx)

        return errors
