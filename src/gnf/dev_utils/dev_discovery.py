import logging

import requests
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.algo_utils import BasicAccount
from gnf.enums import CoreGNodeRole
from gnf.schemata import DiscoverycertAlgoCreate_Maker
from gnf.utils import RestfulResponse


LOGGER = logging.getLogger(__name__)


class DevDiscoverer:
    def __init__(self, settings: config.AdaDiscovererSettings):
        self.settings = settings
        self.client: AlgodClient = algo_utils.get_algod_client(config.Algo())
        self.acct: BasicAccount = algo_utils.BasicAccount(
            private_key=self.settings.sk.get_secret_value()
        )
        self.multi: algo_utils.MultisigAccount = (
            api_utils.get_discoverer_account_with_admin(self.acct.addr)
        )
        # self.seed_fund_own_account()
        LOGGER.info("DevDiscoverer Initialized")

    def post_discoverycert_algo_create(self) -> RestfulResponse:
        payload = DiscoverycertAlgoCreate_Maker(
            g_node_alias=config.AdaDiscovererSettings().discovered_ctn_alias,
            old_child_alias_list=config.AdaDiscovererSettings().original_child_alias_list,
            discoverer_addr=self.acct.addr,
            supporting_material_hash="supporting material",
            core_g_node_role=CoreGNodeRole.ConductorTopologyNode,
            micro_lon=config.AdaDiscovererSettings().micro_lon,
            micro_lat=config.AdaDiscovererSettings().micro_lat,
        ).tuple
        api_endpoint = f"{config.Algo().gnf_api_root}/discoverycert-algo-create/"
        r = requests.post(url=api_endpoint, json=payload.as_dict())
