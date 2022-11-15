import json
import logging
from typing import List

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
from gnf.utils import RestfulResponse


logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)



def certify_molly_metermaid() -> None:
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


def create_ta_owner(plant: str) -> DevTaOwner:
    file = f"input_data/eventstore/d1.isone.ver.keene.{plant}.ta-tadeed.specs.hack.json"
    with open(file) as f:
        payload = TadeedSpecsHack_Maker.dict_to_tuple(json.load(f))

    settings = config.TaOwnerSettings()
    ta_owner_acct = BasicAccount()
    settings.sk = SecretStr(ta_owner_acct.sk)
    settings.initial_ta_alias = payload.TerminalAssetAlias
    settings.ta_daemon_api_port = payload.DaemonPort
    ta_owner = DevTaOwner(settings)
    return ta_owner


def create_ta_owners(plants: List[str]) -> List[DevTaOwner]:
    owners: List[DevTaOwner] = []
    for plant in plants:
        owners.append(create_ta_owner(plant))
    return owners


def start_ta_owners(ta_owners: List[DevTaOwner]) -> RestfulResponse:
    started_ta_owners: List[DevTaOwner] = []
    for owner in ta_owners:
        try:
            owner.start()
        except:
            for owner in started_ta_owners:
                owner.stop()
            return RestfulResponse(
                Note=f"Error starting {owner.settings.initial_ta_alias} owner.",
                HttpStatusCode=422,
            )
        started_ta_owners.append(owner)
    return RestfulResponse(Note="Successfully started all TaOwners and TaDaemons")


def create_terminal_asset(ta_owner: DevTaOwner) -> RestfulResponse:
    molly = DevValidator(config.ValidatorSettings())
    rr = ta_owner.request_ta_certification()
    if rr.HttpStatusCode > 200:
        note = (
            f"Stopping demo due to errors in requesting ta certification for "
            f"{ta_owner.settings.initial_ta_alias}" + rr.Note
        )
        return RestfulResponse(Note=note, HttpStatusCode=422)
    pprint(rr)
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

    if rr.HttpStatusCode > 200:
        note = (
            "Stopping demo due to errors certifying terminal asset for "
            f"{ta_owner.settings.initial_ta_alias}" + rr.Note
        )
        return RestfulResponse(Note=note, HttpStatusCode=422)
    pprint(rr)
    return rr


def create_terminal_assets(ta_owners: List[DevTaOwner]) -> RestfulResponse:
    for ta_owner in ta_owners:
        if not isinstance(ta_owner, DevTaOwner):
            return RestfulResponse(
                Note=f"{ta_owner} is not a DevTaOwner!", HttpStatusCode=422
            )
    for ta_owner in ta_owners:
        rr = create_terminal_asset(ta_owner)
        if rr.HttpStatusCode > 200:
            for ta_owner in ta_owners:
                ta_owner.stop()
            return rr
    return RestfulResponse(Note="Success with create_terminal_assets")


def create_new_ctn():
    ada = DevDiscoverer(settings=config.DiscovererSettings())
    rr = ada.post_discoverycert_algo_create()
    LOGGER.info("Ada received response to discoverycert algo")


demo_plant_names: List[str] = [
    "acacia",
    "acca",
    "acorus",
    "aechmea",
    "aeonium",
    "agapetes",
    "agave",
    "aloe",
    "apple",
    "beech",
    "beet",
    "begonia",
    "billbergia",
    "biophytum",
    "birch",
    "blechnum",
    "bouvardia",
    "brunfelsia",
    "buxus",
    "cactus",
    "calathea",
    "callisia",
    "camellia",
    "campanula",
    "capsicum",
    "caryota",
    "cattleya",
    "ceropegia",
    "chenolle",
    "cherimoya",
    "chestnut",
    "citronella",
    "cleyera",
    "clivia",
    "coccoloba",
    "coconut",
    "coffea",
    "coleus",
    "colmanara",
    "columnea",
    "cordyline",
    "corokia",
    "costus",
    "cottonwood",
    "cotyledon",
    "crassula",
    "crinum",
    "crossandra",
    "cuphea",
    "cyanotis",
    "cycas",
    "cyclamen",
    "cyperus",
    "datura",
    "dionaea",
    "dipladenia",
    "dischidia",
    "dracaena",
    "drosera",
    "duchesnea",
    "echeveria",
    "elm",
    "encyclia",
    "epidendrum",
    "episcia",
    "erica",
    "eucharis",
    "euphorbia",
    "exacum",
    "fatshedera",
    "fatsia",
    "ficus",
    "fir",
    "fittonia",
    "fuchsia",
    "gardenia",
    "gasteria",
    "gloriosa",
    "gongora",
    "guzmania",
    "gynura",
    "haemaria",
    "haworth",
    "haworthia",
    "hedera",
    "hedera",
    "hibiscus",
    "hoffmannia",
    "holly",
    "howea",
    "hoya",
    "hydrangea",
    "impatiens",
    "iresine",
    "ixora",
    "jacobinia",
    "jasmine",
    "jatropha",
    "juniper",
    "kalanchoe",
    "kale",
    "kohleria",
    "laelia",
    "lantana",
    "laurus",
    "lemon",
    "lepanthes",
    "lettuce",
    "lilium",
    "lilium",
    "lily",
    "liriope",
    "livistona",
    "macodes",
    "mallow",
    "mansoa",
    "maple",
    "maranta",
    "maxillaria",
    "medinilla",
    "miltonia",
    "mimosa",
    "molineria",
    "monstera",
    "murraya",
    "mushroom",
    "myrtle",
    "neoregelia",
    "nepenthes",
    "nerine",
    "nertera",
    "nettle",
    "oak",
    "oleander",
    "oncidium",
    "orange",
    "orange",
    "pandanus",
    "passiflora",
    "pellaea",
    "pellionia",
    "pentas",
    "peperomia",
    "petunia",
    "phoenix",
    "pilea",
    "pine",
    "pineapple",
    "pisonia",
    "pleione",
    "plumbago",
    "polyscias",
    "primrose",
    "primula",
    "punica",
    "quinoi",
    "redwood",
    "rhapis",
    "rhoeo",
    "rivina",
    "rochea",
    "rose",
    "ruellia",
    "saffron",
    "sanchezia",
    "spruce",
    "stapelia",
    "strelitzia",
    "thistle",
    "thistle",
    "thunia",
    "tolmiea",
    "tomato",
    "umbrella",
    "umbrella",
    "violet",
    "wasabi",
    "willow",
    "yarrow",
    "zinnia"
 ]