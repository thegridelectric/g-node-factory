import logging

from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
import gnf.load_dev_data as load_dev_data
from gnf import PythonTaDaemon
from gnf.dev_utils import DevHomeowner
from gnf.dev_utils import DevValidator
from gnf.g_node_factory_db import GNodeFactoryDb


logging.basicConfig(level="INFO")

settingsAlgo = config.Algo()

client: AlgodClient = algo_utils.get_algod_client(settingsAlgo)
algo_setup.dev_fund_admin_and_graveyard(config.GnfSettings())
factory = GNodeFactoryDb(config.GnfSettings())
load_dev_data.main()
graveyard = factory.graveyard_account
admin = factory.admin_account

holly = DevHomeowner(
    settings=config.HollyHomeownerSettings(),
    ta_daemon_addr=config.SandboxDemo().holly_ta_daemon_addr,
    validator_addr=config.SandboxDemo().molly_metermaid_addr,
    initial_terminal_asset_alias=config.SandboxDemo().initial_holly_ta_alias,
)

ta_multi = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[admin.addr, holly.ta_daemon_addr, holly.acct.addr],
)


molly = DevValidator(config.MollyMetermaidSettings())

cert_idx = api_utils.get_validator_cert_idx(validator_addr=molly.acct.addr)
if cert_idx is not None:
    raise Exception(
        f"There is already a Validator Certificate for Molly! Please ./sandbox reset and start the demo over."
    )
payload = molly.generate_create_tavalidatorcert_algo()
cert_idx = factory.create_tavalidatorcert_algo_received(payload)

payload = molly.generate_transfer_tavalidatorcert_algo(cert_idx=cert_idx)
factory.transfer_tavalidatorcert_algo_received(payload)


payload = molly.generate_create_tadeed_algo(
    terminal_asset_alias=holly.initial_terminal_asset_alias,
)
atomic_metering_node = factory.create_tadeed_algo_received(payload)
ta_deed_idx = atomic_metering_node.ownership_deed_nft_id


payload = holly.opt_into_original_deed()

python_ta_daemon = PythonTaDaemon(
    sk=config.HollyTaDaemonSettings().sk.get_secret_value(),
    ta_owner_addr=config.SandboxDemo().holly_homeowner_addr,
    algo_settings=config.Algo(),
)

python_ta_daemon.signandsubmit_mtx_algo_received(payload)

payload = molly.generate_transfer_tadeed_algo(
    ta_deed_idx=ta_deed_idx,
    ta_owner_addr=holly.acct.addr,
    ta_daemon_addr=python_ta_daemon.acct.addr,
    micro_lat=45666353,
    micro_lon=-68691705,
)

factory.transfer_tadeed_algo_received(payload)
