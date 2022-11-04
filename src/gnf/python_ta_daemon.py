import logging

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import NewTadeedSend
from gnf.schemata import NewTadeedSend_Maker
from gnf.schemata import OldTadeedAlgoReturn


LOGGER = logging.getLogger(__name__)


class PythonTaDaemon:
    def __init__(self, sk: str, ta_owner_addr: str, algo_settings: config.Algo):
        self.algo_settings = algo_settings
        self.client: AlgodClient = algo_utils.get_algod_client(algo_settings)
        self.acct: BasicAccount = BasicAccount(private_key=sk)
        self.ta_owner_addr = ta_owner_addr
        LOGGER.info("TaOwner Smart Daemon Initialized")

    def send_message_to_gnf(self, payload: NewTadeedSend):
        """Stub for when there is a mechanism (probably FastAPI) for validators  sending
        messages to GNodeFactory.

        Args:
            payload: Any valid payload in the API for sending
        """
        pass

    ##########################
    # Messages Received
    ##########################

    def initial_tadeed_algo_optin_received(self, payload: InitialTadeedAlgoOptin):
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

    def new_tadeed_algo_optin_received(
        self, payload: NewTadeedAlgoOptin
    ) -> NewTadeedSend:
        """
        Checks that payload.NewDeedIdx is a TaDeed

        Args:
            payload: NewTadeedAlgoOptin
        """

        txn = transaction.AssetOptInTxn(
            sender=self.acct.addr,
            index=payload.NewTaDeedIdx,
            sp=self.client.suggested_params(),
        )

        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise Exception(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())
        # FIX
        # Ready for new TaDeed -> let GNodeFactory know
        payload = NewTadeedSend_Maker(
            new_ta_deed_idx=payload.NewTaDeedIdx,
            old_ta_deed_idx=payload.OldTaDeedIdx,
            ta_daemon_addr=self.acct.addr,
            validator_addr=payload.ValidatorAddr,
            signed_tadeed_optin_txn=encoding.msgpack_encode(signed_txn),
        ).tuple
        self.send_message_to_gnf(payload)
        LOGGER.info(f"Asking for transfer of new TaDeed {payload.NewTaDeedIdx}")
        return payload

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
        LOGGER.info(f"Returned TaDeed {payload.OldTaDeedIdx} to GNodeFactory Admin")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())
