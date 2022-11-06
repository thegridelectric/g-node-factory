import logging

import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.dev_utils import DevHomeowner
from gnf.dev_utils import DevValidator
from gnf.g_node_factory_db import GNodeFactoryDb


logging.basicConfig(level="INFO")


def main():
    algo_setup.dev_fund_admin_and_graveyard(config.GnfSettings())
    factory = GNodeFactoryDb(config.GnfSettings())

    holly = DevHomeowner(
        settings=config.HollyHomeownerSettings(),
        ta_daemon_addr=config.SandboxDemo().holly_ta_daemon_addr,
        validator_addr=config.SandboxDemo().molly_metermaid_addr,
        initial_terminal_asset_alias=config.SandboxDemo().initial_holly_ta_alias,
    )

    molly = DevValidator(config.MollyMetermaidSettings())

    cert_idx = api_utils.get_validator_cert_idx(validator_addr=molly.acct.addr)
    if cert_idx is not None:
        raise Exception(
            f"There is already a Validator Certificate for Molly! Please ./sandbox reset and start the demo over."
        )
    r = molly.post_create_tavalidatorcert_algo()

    if r.HttpStatusCode > 200:
        raise Exception("Stopping demo due to errors")

    # payload = molly.generate_initial_tadeed_algo_create(
    #     terminal_asset_alias=holly.initial_terminal_asset_alias,
    # )
    # atomic_metering_node = factory.initial_tadeed_algo_create_received(payload)
    # ta_deed_idx = atomic_metering_node.ownership_deed_nft_id

    # holly.post_initial_tadeed_algo_optin()

    # payload = molly.generate_initial_tadeed_algo_transfer(
    #     ta_deed_idx=ta_deed_idx,
    #     ta_daemon_addr=config.SandboxDemo().holly_ta_daemon_addr,
    #     ta_owner_addr=holly.acct.addr,
    #     micro_lat=45666353,
    #     micro_lon=-68691705,
    # )

    # factory.initial_tadeed_algo_transfer_received(payload)


if __name__ == "__main__":
    main()
