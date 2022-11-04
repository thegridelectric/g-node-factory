import logging

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
import gnf.errors as errors
from gnf.algo_utils import BasicAccount
from gnf.algo_utils import MultisigAccount

# Schemata sent by homeowner
from gnf.schemata import TadeedAlgoOptinInitial
from gnf.schemata import TadeedAlgoOptinInitial_Maker


LOGGER = logging.getLogger(__name__)


class DevHomeowner:
    def __init__(
        self,
        settings: config.HollyHomeownerSettings,
        ta_daemon_addr: str,
        validator_addr: str,
        initial_terminal_asset_alias: str,
    ):
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(self.settings.algo)
        self.acct: BasicAccount = BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.ta_daemon_addr = ta_daemon_addr

        self.validator_addr = validator_addr
        self.validator_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[config.Algo().gnf_admin_addr, validator_addr],
        )
        self.initial_terminal_asset_alias = initial_terminal_asset_alias
        self.seed_fund_own_account()
        LOGGER.info("HollyHomeowner Initialized")

    ##########################
    # Messages Sent
    ##########################

    def opt_into_original_deed(self) -> TadeedAlgoOptinInitial:
        """
         - Sends 50 algos to TaDaemon acct
         - Sends TadeedAlgoOptinInitial to TaDaemon, with signed
         funding txn for proof of identity.

        Returns:
            TadeedAlgoOptinInitial:
        """
        required_algos = config.Algo().ta_deed_consideration_algos
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

        payload = TadeedAlgoOptinInitial_Maker(
            terminal_asset_alias=self.initial_terminal_asset_alias,
            ta_owner_addr=self.acct.addr,
            validator_addr=self.validator_addr,
            signed_initial_daemon_funding_txn=encoding.msgpack_encode(signed_txn),
        ).tuple

        return payload

    ##########################
    # dev methods
    ########################
    def seed_fund_own_account(self):
        algos = config.Algo().ta_deed_consideration_algos + 1
        if algo_utils.algos(self.acct.addr) < algos:
            algo_setup.dev_fund_account(
                settings_algo=self.settings.algo,
                to_addr=self.acct.addr,
                amt_in_micros=10**6 * algos,
            )
        LOGGER.info(
            f"HollyHomeowner acct {self.acct.addr_short_hand} balance: ~{algo_utils.algos(self.acct.addr)} Algos"
        )
