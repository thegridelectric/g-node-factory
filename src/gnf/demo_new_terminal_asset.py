import logging

from rich.pretty import pprint

import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.dev_utils import DevHomeowner
from gnf.dev_utils import DevValidator
from gnf.schemata import BasegnodeGt_Maker


logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)


def main():
    algo_setup.dev_fund_admin_and_graveyard(config.GnfSettings())

    holly = DevHomeowner(
        settings=config.HollyHomeownerSettings(),
        ta_daemon_port=config.SandboxDemo().holly_daemon_port,
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
    r = molly.post_tavalidatorcert_algo_create()

    if r.HttpStatusCode > 200:
        pprint(r)
        raise Exception("Stopping demo due to errors")

    ta_alias = holly.initial_terminal_asset_alias
    LOGGER.info(
            f"Post to GnfRestAPI/initial-tadeed-algo-create to create a TaDeed for {ta_alias}"
        )
    r = molly.post_initial_tadeed_algo_create(
        terminal_asset_alias=ta_alias,
    )
    pprint(r)

    if r.HttpStatusCode > 200:
        raise Exception("Stopping demo due to errors")

    atm_gt = BasegnodeGt_Maker.dict_to_tuple(r.PayloadAsDict)

    ta_deed_idx = atm_gt.OwnershipDeedNftId

    holly.post_initial_tadeed_algo_optin()

    r = molly.post_initial_tadeed_algo_transfer(
        ta_deed_idx=ta_deed_idx,
        ta_daemon_addr=config.SandboxDemo().holly_ta_daemon_addr,
        ta_owner_addr=holly.acct.addr,
        micro_lat=45666353,
        micro_lon=-68691705,
    )

    if r.HttpStatusCode > 200:
        pprint(r)
        raise Exception("Stopping demo due to errors")


if __name__ == "__main__":
    main()
