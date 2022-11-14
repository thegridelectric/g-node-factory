import logging

import requests_async as requests
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient
from asgiref.sync import sync_to_async
from rich.pretty import pprint

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
import gnf.errors as errors
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount

# Schemata sent by homeowner
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import InitialTadeedAlgoOptin_Maker
from gnf.schemata import TerminalassetCertifyHack_Maker


LOGGER = logging.getLogger(__name__)


class DevTaOwner:
    def __init__(
        self,
        settings: config.TaOwnerSettings,
    ):
        LOGGER.info(f"Initializing TaOwner for {settings.initial_ta_alias}")

        self.settings = settings
        self.client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        self.acct: BasicAccount = BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.validator_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[
                self.settings.public.gnf_admin_addr,
                self.settings.validator_addr,
            ],
        )
        ta_daemon_acct: BasicAccount = BasicAccount()
        self.ta_daemon_sk: str = ta_daemon_acct.sk
        self.ta_daemon_addr: str = ta_daemon_acct.addr
        self.settings.ta_daemon_addr: str = ta_daemon_acct.addr  # REMOVE!!!
        self.seed_fund_own_account()

    ##########################
    # Messages Sent
    ##########################

    async def request_ta_certification(self) -> None:
        ta_alias = self.settings.initial_ta_alias
        payload = TerminalassetCertifyHack_Maker(terminal_asset_alias=ta_alias).tuple
        LOGGER.info(f"Requesting certification for {ta_alias}")
        api_endpoint = (
            f"{self.settings.public.molly_api_root}/terminalasset-certification/"
        )
        r = await requests.post(url=api_endpoint, json=payload.as_dict())
        return r

    def post_initial_tadeed_algo_optin(self) -> InitialTadeedAlgoOptin:
        """
         - Sends 50 algos to TaDaemon acct
         - Sends InitialTadeedAlgoOptin to TaDaemon, with signed
         funding txn for proof of identity.

        Returns:
            InitialTadeedAlgoOptin:
        """
        required_algos = config.GnfPublic().ta_deed_consideration_algos
        txn = transaction.PaymentTxn(
            sender=self.acct.addr,
            receiver=self.ta_daemon_addr,
            amt=required_algos * 10**6,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except:
            raise errors.AlgoError(f"Failure sending transaction")
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

        payload = InitialTadeedAlgoOptin_Maker(
            terminal_asset_alias=self.settings.initial_ta_alias,
            ta_owner_addr=self.acct.addr,
            validator_addr=self.settings.validator_addr,
            signed_initial_daemon_funding_txn=encoding.msgpack_encode(signed_txn),
            ta_daemon_private_key=self.ta_daemon_sk,
        ).tuple
        api_endpoint = f"{self.settings.ta_daemon_api_root}/initial-tadeed-algo-optin/"
        r = requests.post(url=api_endpoint, json=payload.as_dict())
        LOGGER.info("Sent InitialTadeedAlgoOptin")
        pprint(r.json())
        return r

    ##########################
    # dev methods
    ########################
    def seed_fund_own_account(self):
        algos = self.settings.public.ta_deed_consideration_algos + 1
        if algo_utils.algos(self.acct.addr) < algos:
            algo_setup.dev_fund_account(
                settings=self.settings,
                to_addr=self.acct.addr,
                amt_in_micros=10**6 * algos,
            )
        LOGGER.info(
            f"HollyHomeowner acct {self.acct.addr_short_hand} balance: ~{algo_utils.algos(self.acct.addr)} Algos"
        )
