import logging

import dotenv
from rich.pretty import pprint

import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.dev_utils import DevTaOwner
from gnf.dev_utils import DevValidator
from gnf.schemata import BasegnodeGt_Maker


logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)


def main():
    algo_setup.dev_fund_admin_and_graveyard(
        config.VanillaSettings(_env_file=dotenv.find_dotenv())
    )

    # holly = DevTaOwner(settings=config.TaOwnerSettings())

    molly = DevValidator(config.ValidatorSettings())

    cert_idx = api_utils.get_validator_cert_idx(validator_addr=molly.acct.addr)
    if cert_idx is not None:
        raise Exception(
            f"There is already a Validator Certificate for Molly! Please ./sandbox reset and start the demo over."
        )
    rr = molly.post_tavalidatorcert_algo_create()
    pprint(rr)
    if rr.HttpStatusCode > 200:

        raise Exception("Stopping demo due to errors")

    # rr = holly.request_ta_certification()
    # pprint(rr)
    # if rr.HttpStatusCode > 200:
    #     raise Exception("Stopping demo due to errors")

    # atm_gt = BasegnodeGt_Maker.dict_to_tuple(r.PayloadAsDict)

    # ta_deed_idx = atm_gt.OwnershipDeedNftId

    # holly.post_initial_tadeed_algo_optin()

    # r = molly.certify_terminal_asset(
    #     ta_deed_idx=ta_deed_idx,
    #     ta_daemon_addr=holly.settings.ta_daemon_addr,
    #     ta_owner_addr=holly.acct.addr,
    #     micro_lat=holly.settings.micro_lat,
    #     micro_lon=-holly.settings.micro_lon,
    # )

    # if r.HttpStatusCode > 200:
    #     pprint(r)
    #     raise Exception("Stopping demo due to errors")


if __name__ == "__main__":
    main()
