import logging

from rich.pretty import pprint

import gnf.config as config
from gnf.dev_utils.dev_discovery import DevDiscoverer


logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


def main():
    ada = DevDiscoverer(settings=config.AdaDiscovererSettings())
    r = ada.post_discoverycert_algo_create()
    LOGGER.info("Ada received response to discoverycert algo")
    pprint(r.json())


if __name__ == "__main__":
    main()
