import logging

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
from gnf.enums import CoreGNodeRole
from gnf.g_node_factory_db import GNodeFactoryDb
from gnf.python_ta_daemon import PythonTaDaemon
from gnf.schemata import DiscoverycertAlgoCreate_Maker


logging.basicConfig(level="INFO")


def main():
    molly_addr = config.SandboxDemo().molly_metermaid_addr

    factory = GNodeFactoryDb(config.GnfSettings())

    python_ta_daemon = PythonTaDaemon(
        sk=config.HollyTaDaemonSettings().sk.get_secret_value(),
        ta_owner_addr=config.SandboxDemo().holly_homeowner_addr,
        algo_settings=config.Algo(),
    )

    ada = algo_utils.BasicAccount(config.AdaDiscovererSettings().sk.get_secret_value())

    payload = DiscoverycertAlgoCreate_Maker(
        g_node_alias=config.AdaDiscovererSettings().discovered_ctn_alias,
        old_child_alias_list=config.AdaDiscovererSettings().original_child_alias_list,
        discoverer_addr=ada.addr,
        supporting_material_hash="supporting material",
        core_g_node_role=CoreGNodeRole.ConductorTopologyNode,
        micro_lon=config.AdaDiscovererSettings().micro_lon,
        micro_lat=config.AdaDiscovererSettings().micro_lat,
    ).tuple

    optin_payload = factory.discoverycert_algo_create_received(payload)

    python_ta_daemon.optin_tadeed_algo_received(optin_payload)

    created_assets = factory.client.account_info(factory.admin_account.addr)[
        "created-assets"
    ]
    ta_deeds = list(
        filter(lambda x: x["params"]["unit-name"] == "TADEED", created_assets)
    )
    new_ta_deed = list(
        filter(
            lambda x: x["params"]["name"] == "d1.isone.ver.keene.pwrs.holly.ta",
            ta_deeds,
        )
    )
    new_ta_deed_idx = new_ta_deed[0]["index"]
    old_ta_deed_idx = api_utils.get_tadeed_cert_idx(
        "d1.isone.ver.keene.holly.ta", molly_addr
    )

    exchange_payload = factory.generate_exchange_tadeed_algo(
        old_ta_deed_idx=old_ta_deed_idx,
        new_ta_deed_idx=new_ta_deed_idx,
        validator_addr=molly_addr,
        ta_owner_addr=python_ta_daemon.ta_owner_addr,
        ta_daemon_addr=python_ta_daemon.acct.addr,
    )

    python_ta_daemon.exchange_tadeed_algo_received(exchange_payload)

    # To check that the deeds are in the correct place:

    python_ta_daemon.client.account_info(python_ta_daemon.acct.addr)

    python_ta_daemon.client.account_info(factory.admin_account.addr)


if __name__ == "__main__":
    main()
