####################
# Under Construction
#####################
import logging
from typing import Optional

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.algo_utils import PendingTxnResponse
from gnf.schemata import OptinTadeedAlgo
from gnf.schemata import TadeedAlgoExchange
from gnf.schemata import TadeedAlgoOptinInitial


# sent by the daemon

# types received by the daemon


LOGGER = logging.getLogger(__name__)


class PythonTaDaemon:
    def __init__(self, sk: str, ta_owner_addr: str, algo_settings: config.Algo):
        self.algo_settings = algo_settings
        self.client: AlgodClient = algo_utils.get_algod_client(algo_settings)
        self.acct: BasicAccount = BasicAccount(private_key=sk)
        self.ta_owner_addr = ta_owner_addr
        self.ta_multi: MultisigAccount = self.get_ta_multi()
        LOGGER.info("TaOwner Smart Daemon Initialized")

    def get_ta_multi(self) -> MultisigAccount:
        """
        Returns:
            Multisig: returns the multisig ordered [gnfadmin, daemon, taOwner] with
            signing threshold 2
        """
        addresses = [
            self.algo_settings.gnf_admin_addr,
            config.SandboxDemo().holly_ta_daemon_addr,
            config.SandboxDemo().holly_homeowner_addr,
        ]
        return MultisigAccount(version=1, threshold=2, addresses=addresses)

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
            tx_id = self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

    def exchange_tadeed_algo_received(self, payload: TadeedAlgoExchange):
        """
         - Sign and submit the AssetTransfer mtx, which will send the old deed from
        the ta_multi acct to the GNodeFactory admin acct.

        Args:
            payload: TadeedAlgoExchange
        """
        mtx = encoding.future_msgpack_decode(payload.OldDeedTransferMtx)
        mtx.sign(self.acct.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except Exception as e:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")
