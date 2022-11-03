####################
# Under Construction
#####################
import logging
from typing import Optional

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount
from gnf.algo_utils import PendingTxnResponse
from gnf.schemata import OptinTadeedAlgo
from gnf.schemata import SignandsubmitMtxAlgo
from gnf.schemata import TadeedAlgoExchange


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

    def signandsubmit_mtx_algo_received(
        self, payload: SignandsubmitMtxAlgo
    ) -> Optional[PendingTxnResponse]:
        """Checks that the transaction is a Multisig transaction where
        the TaOwner is one of the addresses and the TaOwner has signed
        the transaction.

        Also checks that payload.SignerAddress is TaDaemon address.
        Then signs and submits

        Args:
            payload: SignandsubmitMtxAlgo)

        Returns:
            PendingTxnResponse of submitted Mtx if the original signer is ta_owner, otherwise None
        """
        ta_owner_address_as_bytes = encoding.decode_address(self.ta_owner_addr)
        mtx = encoding.future_msgpack_decode(payload.Mtx)
        x = list(
            filter(
                lambda x: x.public_key == ta_owner_address_as_bytes,
                mtx.multisig.subsigs,
            )
        )
        if len(x) == 0:
            LOGGER.info(
                f"Ignoring signandsubmit. ta_owner ..{self.ta_owner_addr} not in mtx addresses"
            )
            return
        ta_owner_subsig = x[0]
        if ta_owner_subsig.signature is None:
            LOGGER.info(
                f"Ignoring signandsubmit. ta_owner ..{self.ta_owner_addr} did not sign"
            )
        if payload.SignerAddress != self.acct.addr:
            LOGGER.info(f"Igoring signandsubmit. My acct not the SignerAddress")
            return None

        mtx.sign(self.acct.sk)
        try:
            response: PendingTxnResponse = algo_utils.send_signed_mtx(
                client=self.client, mtx=mtx
            )
        except Exception as e:
            LOGGER.warning(f"Tried to sign transaction but there was an error.\n {e}")

    def optin_tadeed_algo_received(self, payload: OptinTadeedAlgo):
        """
        Checks that payload.NewDeedIdx is a TaDeed

        Args:
            payload: OptinTadeedAlgo
        """
        # TODO: check that payload.NewDeedIdx is a TaDeed
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
        # r = algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

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
