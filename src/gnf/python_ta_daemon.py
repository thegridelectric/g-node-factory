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
from gnf.utils import RestfulResponse


LOGGER = logging.getLogger(__name__)


class PythonTaDaemon:
    def __init__(self, settings: config.TaDaemonSettings):
        self.settings = settings
        self.client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        self.acct: BasicAccount = BasicAccount(
            private_key=settings.sk.get_secret_value()
        )
        LOGGER.info("TaOwner Smart Daemon Initialized")

    ##########################
    # Messages Received
    ##########################

    def initial_tadeed_algo_optin_received(
        self, payload: InitialTadeedAlgoOptin
    ) -> RestfulResponse:
        ta_deed_idx = api_utils.get_tadeed_cert_idx(
            terminal_asset_alias=payload.TerminalAssetAlias,
            validator_addr=payload.ValidatorAddr,
        )
        if ta_deed_idx is None:
            note = f"called when validator {payload.ValidatorAddr[-6:]} did NOT have TADEED for {payload.TerminalAssetAlias}!"
            LOGGER.info(note)
            r = RestfulResponse(
                Note=note,
                HttpStatusCode=422,
            )
            return r

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
        note = f"TaDaemon successfully opted in to Initial TaDeed {ta_deed_idx}"
        LOGGER.info(note)
        r = RestfulResponse(Note=note)
        return r

    def new_tadeed_algo_optin_received(
        self, payload: NewTadeedAlgoOptin
    ) -> RestfulResponse:
        """Opts in to a new (i.e. updated) TaDeed

        Args:
            payload (NewTadeedAlgoOptin): NewTadeedAlgoOptin

        Returns:
            RestfulResponse:  HttpStatusCode 422 if there is a semantic
            issue (e.g. failure sending transaction on blockchain)

            Otherwise, Payload is NewTadeedSend
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
            note = "Failure sending transaction on Algo blockchain"
            r = RestfulResponse(
                Note=note,
                HttpStatusCode=422,
            )
            return r
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

        return_payload = NewTadeedSend_Maker(
            new_ta_deed_idx=payload.NewTaDeedIdx,
            old_ta_deed_idx=payload.OldTaDeedIdx,
            ta_daemon_addr=self.acct.addr,
            validator_addr=payload.ValidatorAddr,
            signed_tadeed_optin_txn=encoding.msgpack_encode(signed_txn),
        ).tuple
        note = f"Opted in to TaDeed {payload.NewTaDeedIdx}, ready for transfer"
        r = RestfulResponse(
            Note=note,
            PayloadTypeName=NewTadeedSend_Maker.type_name,
            PayloadAsDict=return_payload.as_dict(),
        )
        LOGGER.info(f"Opted in to TaDeed {payload.NewTaDeedIdx}, ready for transfer")
        return r

    def old_tadeed_algo_return_received(
        self, payload: OldTadeedAlgoReturn
    ) -> RestfulResponse:
        """
         - Transfer the  old deed back to the GNodeFactory admin acct.

        Args:
            payload: OldTadeedAlgoReturn
        """

        txn = transaction.AssetTransferTxn(
            sender=self.acct.addr,
            receiver=config.GnfPublic().gnf_admin_addr,
            amt=1,
            index=payload.OldTaDeedIdx,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            note = "Failure sending transaction on Algo blockchain"
            r = RestfulResponse(
                Note=note,
                HttpStatusCode=422,
            )
            return r

        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())
        note = f"TaDaemon transferred old TaDeed {payload.OldTaDeedIdx} to GNodeFactoryAdmin"
        LOGGER.info(note)
        r = RestfulResponse(Note=note)
        return r
