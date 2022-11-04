import logging
from re import L
from typing import Optional

from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.algo_utils import BasicAccount

# Schemata sent by discoverer
from gnf.schemata import DiscoverycertAlgoCreate


LOGGER = logging.getLogger(__name__)


class DevDiscoverer:
    def __init__(self, settings: config.AdaDiscovererSettings):
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(self.settings.algo)
        self.acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.multi: algo_utils.MultisigAccount = (
            api_utils.get_discoverer_account_with_admin(self.acct.addr)
        )
        # self.seed_fund_own_account()
        LOGGER.info("DevDiscoverer Initialized")

    def send_message_to_gnf(self, payload: DiscoverycertAlgoCreate):
        """Stub for when there is a mechanism (probably FastAPI) for validators  sending
        messages to GNodeFactory.

        Args:
            payload: Any valid payload in the API for sending
        """
        pass

    ###################
    # Messages sent
    ###################

    def generate_create_discoverycert_algo(
        self, terminal_asset_alias: str
    ) -> DiscoverycertAlgoCreate:

        pass
