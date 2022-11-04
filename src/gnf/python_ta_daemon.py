import logging

from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.schemata import OldTadeedAlgoReturn
from gnf.schemata import OptinTadeedAlgo
from gnf.schemata import TadeedAlgoOptinInitial


LOGGER = logging.getLogger(__name__)


class PythonTaDaemon:
    def __init__(self, sk: str, ta_owner_addr: str, algo_settings: config.Algo):
        self.algo_settings = algo_settings
        self.client: AlgodClient = algo_utils.get_algod_client(algo_settings)
        self.acct: BasicAccount = BasicAccount(private_key=sk)
        self.ta_owner_addr = ta_owner_addr
        LOGGER.info("TaOwner Smart Daemon Initialized")

    ##########################
    # Messages Received
    ##########################

    def tadeed_algo_optin_initial_received(self, payload: TadeedAlgoOptinInitial):
        ta_deed_idx = api_utils.get_tadeed_cert_idx(
            terminal_asset_alias=payload.TerminalAssetAlias,
            validator_addr=payload.ValidatorAddr,
        )
        if ta_deed_idx is None:
            raise Exception(
                f"called when validator {payload.ValidatorAddr[-6:]} did NOT have "
                f"TADEED for {payload.TerminalAssetAlias}!"
            )
        txn = transaction.AssetOptInTxn(
            sender=self.acct.addr,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

    def optin_tadeed_algo_received(self, payload: OptinTadeedAlgo):
        """
        Checks that payload.NewDeedIdx is a TaDeed

        Args:
            payload: OptinTadeedAlgo
        """

        txn = transaction.AssetOptInTxn(
            sender=self.acct.addr,
            index=payload.NewDeedIdx,
            sp=self.client.suggested_params(),
        )

        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

    def old_tadeed_algo_return_received(self, payload: OldTadeedAlgoReturn):
        """
         - Transfer the  old deed back to the GNodeFactory admin acct.

        Args:
            payload: OldTadeedAlgoReturn
        """

        txn = transaction.AssetTransferTxn(
            sender=self.acct.addr,
            receiver=config.Algo().gnf_admin_addr,
            amt=1,
            index=payload.OldTaDeedIdx,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())
