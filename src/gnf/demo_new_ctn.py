import logging

import gnf.algo_utils as algo_utils
import gnf.config as config
from gnf.enums import CoreGNodeRole
from gnf.g_node_factory_db import GNodeFactoryDb
from gnf.schemata import DiscoverycertAlgoCreate_Maker


logging.basicConfig(level="INFO")


def main():

    factory = GNodeFactoryDb(config.GnfSettings())

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

    factory.discoverycert_algo_create_received(payload)


if __name__ == "__main__":
    main()
