import logging

import algo_utils
import api_utils
import config
from algosdk.v2client.algod import AlgodClient
from dev_utils.dev_homeowner import DevHomeowner
from dev_utils.dev_validator import DevValidator
from enums.core_g_node_role_100 import CoreGNodeRole
from g_node_factory_db import GNodeFactoryDb
from python_ta_daemon import PythonTaDaemon
from schemata.create_discoverycert_algo_maker import CreateDiscoverycertAlgo_Maker
from schemata.transfer_discoverycert_algo_maker import TransferDiscoverycertAlgo_Maker


logging.basicConfig(level="INFO")
molly_addr = config.SandboxDemo().molly_metermaid_addr

gnf = GNodeFactoryDb(config.GnfSettings())


python_ta_daemon = PythonTaDaemon(
    sk=config.HollyTaDaemonSettings().sk.get_secret_value(),
    ta_owner_addr=config.SandboxDemo().holly_homeowner_addr,
    algo_settings=config.Algo(),
)

ada = algo_utils.BasicAccount(config.AdaDiscovererSettings().sk.get_secret_value())

payload = CreateDiscoverycertAlgo_Maker(
    g_node_alias=config.AdaDiscovererSettings().discovered_ctn_alias,
    old_child_alias_list=config.AdaDiscovererSettings().original_child_alias_list,
    discoverer_addr=ada.addr,
    supporting_material_hash="supporting material",
    core_g_node_role=CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE,
    micro_lon=config.AdaDiscovererSettings().micro_lon,
    micro_lat=config.AdaDiscovererSettings().micro_lat,
).tuple

optin_payload = gnf.create_discoverycertificate_received(payload)

python_ta_daemon.optin_tadeed_algo_received(optin_payload)

created_assets = gnf.client.account_info(gnf.admin_account.addr)["created-assets"]
ta_deeds = list(filter(lambda x: x["params"]["unit-name"] == "TADEED", created_assets))
new_ta_deed = list(
    filter(
        lambda x: x["params"]["name"] == "d1.isone.ver.keene.pwrs.holly.ta", ta_deeds
    )
)
new_ta_deed_idx = new_ta_deed[0]["index"]
old_ta_deed_idx = api_utils.get_tadeed_cert_idx(
    "d1.isone.ver.keene.holly.ta", molly_addr
)

exchange_payload = gnf.generate_exchange_tadeed_algo(
    old_ta_deed_idx=old_ta_deed_idx,
    new_ta_deed_idx=new_ta_deed_idx,
    validator_addr=molly_addr,
    ta_owner_addr=python_ta_daemon.ta_owner_addr,
    ta_daemon_addr=python_ta_daemon.acct.addr,
)

python_ta_daemon.exchange_tadeed_algo_received(exchange_payload)

# To check that the deeds are in the correct place:

python_ta_daemon.client.account_info(python_ta_daemon.ta_multi.addr)

python_ta_daemon.client.account_info(gnf.admin_account.addr)
