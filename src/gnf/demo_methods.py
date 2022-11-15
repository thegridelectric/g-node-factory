import json
import logging
import time

from pydantic import SecretStr
from rich.pretty import pprint

import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.algo_utils import BasicAccount
from gnf.dev_utils import DevTaOwner
from gnf.dev_utils import DevValidator
from gnf.dev_utils.dev_discovery import DevDiscoverer
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import TadeedSpecsHack_Maker


logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)

molly = DevValidator(config.ValidatorSettings())


def certify_molly_metermaid() -> None:
    cert_idx = api_utils.get_validator_cert_idx(validator_addr=molly.acct.addr)
    if cert_idx is not None:
        raise Exception(
            f"There is already a Validator Certificate for Molly! Please ./sandbox reset and start the demo over."
        )
    rr = molly.post_tavalidatorcert_algo_create()
    pprint(rr)
    if rr.HttpStatusCode > 200:
        raise Exception("Stopping demo due to errors")


def create_terminal_asset(plant: str):
    file = (
        f"input_data/eventstore/dw1.isone.ver.keene.{plant}.ta-tadeed.specs.hack.json"
    )
    with open(file) as f:
        payload = TadeedSpecsHack_Maker.dict_to_tuple(json.load(f))
    settings = config.TaOwnerSettings()
    ta_owner_acct = BasicAccount()
    settings.sk = SecretStr(ta_owner_acct.sk)
    settings.initial_ta_alias = payload.TerminalAssetAlias
    ta_owner = DevTaOwner(settings)
    LOGGER.info("Waiting 5 seconds to let daemon uvicorn start up")
    time.sleep(5)

    rr = ta_owner.request_ta_certification()
    pprint(rr)
    if rr.HttpStatusCode > 200:
        raise Exception("Stopping demo due to errors in creating deed for ")

    terminal_asset = BasegnodeGt_Maker.dict_to_tuple(rr.PayloadAsDict)
    ta_deed_idx = terminal_asset.OwnershipDeedNftId
    LOGGER.info(f"Made TaDeed {ta_deed_idx} for {terminal_asset.Alias}")

    rr = molly.certify_terminal_asset(
        ta_deed_idx=ta_deed_idx,
        ta_daemon_addr=BasicAccount(ta_owner.ta_daemon_sk).addr,
        ta_owner_addr=ta_owner.acct.addr,
        micro_lat=ta_owner.settings.micro_lat,
        micro_lon=ta_owner.settings.micro_lon,
    )

    pprint(rr)
    if rr.HttpStatusCode > 200:
        raise Exception("Stopping demo due to errors")


def create_new_ctn():
    ada = DevDiscoverer(settings=config.DiscovererSettings())
    r = ada.post_discoverycert_algo_create()
    LOGGER.info("Ada received response to discoverycert algo")
