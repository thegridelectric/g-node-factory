import logging
from typing import Optional

import algo_utils
import api_utils
import config
import dev_utils.algo_setup
from algo_utils import BasicAccount
from algo_utils import MultisigAccount
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

# Schemata sent by homeowner
from schemata.signandsubmit_mtx_algo_maker import SignandsubmitMtxAlgo
from schemata.signandsubmit_mtx_algo_maker import SignandsubmitMtxAlgo_Maker


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
        self.ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[config.Algo().gnf_admin_addr, ta_daemon_addr, self.acct.addr],
        )
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

    def opt_into_original_deed(self) -> SignandsubmitMtxAlgo:
        """
         - Sends 50 algos to ta_multi acct
         - Gets TaDeedIdx from ValidatorMulti acct
         - Creates and signs TaDeed Optin for ta_multi as an mtx
         - Sends mtx to daemon using signandsubmit payload

        Returns:
            SignandsubmitMtxAlgo:
        """
        required_algos = config.Algo().ta_deed_consideration_algos
        dev_utils.algo_setup.dev_fund_to_min(self.ta_multi.addr, required_algos)
        LOGGER.info(f"ta_multi funded with {required_algos} Algos")

        ta_deed_idx = api_utils.get_tadeed_cert_idx(
            terminal_asset_alias=self.initial_terminal_asset_alias,
            validator_addr=self.validator_addr,
        )
        if ta_deed_idx is None:
            raise Exception(
                f"called when validator {self.validator_addr[-6:]} did NOT have "
                f"TADEED for {self.initial_terminal_asset_alias}!"
            )
        txn = transaction.AssetOptInTxn(
            sender=self.ta_multi.addr,
            index=ta_deed_idx,
            sp=self.client.suggested_params(),
        )
        mtx = self.ta_multi.create_mtx(txn)
        mtx.sign(self.acct.sk)
        payload = SignandsubmitMtxAlgo_Maker(
            signer_address=self.ta_daemon_addr,
            mtx=encoding.msgpack_encode(mtx),
            threshold=2,
            addresses=[
                config.Algo().gnf_admin_addr,
                self.ta_daemon_addr,
                self.acct.addr,
            ],
        ).tuple
        return payload

    ##########################
    # dev methods
    ########################
    def seed_fund_own_account(self):
        algos = config.Algo().ta_deed_consideration_algos + 1
        if algo_utils.algos(self.acct.addr) < algos:
            dev_utils.algo_setup.dev_fund_account(
                settings_algo=self.settings.algo,
                to_addr=self.acct.addr,
                amt_in_micros=10**6 * algos,
            )
        LOGGER.info(
            f"HollyHomeowner acct {self.acct.addr_short_hand} balance: ~{algo_utils.algos(self.acct.addr)} Algos"
        )
