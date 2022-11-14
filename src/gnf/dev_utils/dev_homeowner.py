import logging
import subprocess

import requests
import requests_async
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
import gnf.errors as errors
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount

# Schemata sent by homeowner
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import InitialTadeedAlgoOptin_Maker
from gnf.schemata import TadaemonSkHack_Maker
from gnf.schemata import TerminalassetCertifyHack_Maker
from gnf.utils import RestfulResponse


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
        self.seed_fund_own_account()
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
        self.settings.ta_daemon_addr: str = ta_daemon_acct.addr
        self.ta_daemon_api_root = (
            f"{self.settings.ta_daemon_api_fqdn}:{self.settings.ta_daemon_api_port}"
        )
        self.ta_daemon_process: subprocess.Popen = self.start_ta_daemon()
        rr: RestfulResponse = self.post_daemon_secrets_hack()
        if rr.HttpStatusCode > 200:
            raise Exception(f"Failed to spawn TaDaemon: {rr.Note}")

    ##########################
    # Messages Sent
    ##########################

    def post_daemon_secrets_hack(self) -> RestfulResponse:
        payload = TadaemonSkHack_Maker(
            ta_owner_addr=self.acct.addr, ta_daemon_sk=self.ta_daemon_sk
        ).tuple
        api_endpoint = f"{self.ta_daemon_api_root}/sk-hack/"
        r = requests.post(url=api_endpoint, json=payload.as_dict())
        if r.status_code > 200:
            if r.status_code == 422:
                note = f"Error posting sk to daemon: " + r.json()["detail"]
            else:
                note = r.reason
            rr = RestfulResponse(Note=note, HttpStatusCode=422)
            return rr
        return RestfulResponse(Note="Success getting sk to daemon")

    def start_ta_daemon(self) -> subprocess.Popen:
        LOGGER.info("Starting ta Daemon")
        cmd = f"uvicorn gnf.ta_daemon_rest_api:app --reload --port {self.settings.ta_daemon_api_port}"
        pr = subprocess.Popen(cmd.split())
        return pr

    async def request_ta_certification(self) -> RestfulResponse:
        ta_alias = self.settings.initial_ta_alias
        payload = TerminalassetCertifyHack_Maker(
            terminal_asset_alias=ta_alias,
            ta_daemon_api_fqdn=self.settings.ta_daemon_api_fqdn,
            ta_daemon_api_port=self.settings.ta_daemon_api_port,
            ta_daemon_addr=self.settings.ta_daemon_addr,
        ).tuple

        LOGGER.info(f"Requesting certification for {ta_alias}")
        api_endpoint = (
            f"{self.settings.public.molly_api_root}/terminalasset-certification/"
        )
        r = await requests_async.post(url=api_endpoint, json=payload.as_dict())
        if r.status_code > 200:
            if r.status_code == 422:
                note = f"Error posting sk to daemon: " + r.json()["detail"]
            else:
                note = r.reason
            rr = RestfulResponse(Note=note, HttpStatusCode=422)
            return rr
        rr = await self.post_initial_tadeed_algo_optin()
        return rr

    async def post_initial_tadeed_algo_optin(self) -> RestfulResponse:
        """
         - Sends 50 algos to TaDaemon acct
         - Sends InitialTadeedAlgoOptin to TaDaemon, with signed
         funding txn for proof of identity.

        Returns:
            RestfulResponse
        """
        required_algos = config.GnfPublic().ta_deed_consideration_algos
        txn = transaction.PaymentTxn(
            sender=self.acct.addr,
            receiver=self.settings.ta_daemon_addr,
            amt=required_algos * 10**6,
            sp=self.client.suggested_params(),
        )
        signed_txn = txn.sign(self.acct.sk)
        try:
            self.client.send_transaction(signed_txn)
        except Exception as e:
            return RestfulResponse(
                Note=f"Algorand Failure sending transaction: {e}", HttpStatusCode=422
            )
        algo_utils.wait_for_transaction(self.client, signed_txn.get_txid())

        payload = InitialTadeedAlgoOptin_Maker(
            terminal_asset_alias=self.settings.initial_ta_alias,
            ta_owner_addr=self.acct.addr,
            validator_addr=self.settings.validator_addr,
            signed_initial_daemon_funding_txn=encoding.msgpack_encode(signed_txn),
            ta_daemon_private_key=self.ta_daemon_sk,
        ).tuple
        api_endpoint = f"{self.ta_daemon_api_root}/initial-tadeed-algo-optin/"
        r = await requests_async.post(url=api_endpoint, json=payload.as_dict())
        if r.status_code > 200:
            if r.status_code == 422:
                note = "Issue with InitialTadeedAlgoOptin" + r.json()["detail"]
            else:
                note = r.reason
            rr = RestfulResponse(Note=note, HttpStatusCode=422)
            return rr
        return RestfulResponse(**r.json())

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
