import logging

import algo_utils
import config
from algo_utils import MultisigAccount
from algosdk import account
from algosdk import encoding
from algosdk.future import transaction
from algosdk.future.transaction import MultisigTransaction
from algosdk.v2client.algod import AlgodClient
from config import Algo
from config import GnfSettings
from config import HollyTaDaemonSettings
from dev_utils import algo_setup
from dev_utils.algo_setup import FUNDING_AMOUNT
from errors import SchemaError
from g_node_factory_db import GNodeFactoryDb


logging.basicConfig(level="INFO")

from schemata.create_tadeed_algo_maker import CreateTadeedAlgo_Maker


####################
# Helpers and config
####################
DEED_ALIAS = "My Deed just for demo"

algo_settings: Algo = config.Algo()
gnf_settings: GnfSettings = config.GnfSettings()
holly_ta_daemon_settings: HollyTaDaemonSettings = config.HollyTaDaemonSettings()

algod_client: AlgodClient = algo_utils.get_algod_client(algo_settings)
sp = algod_client.suggested_params()


class Account:
    def __init__(self, alias: str, private_key) -> None:
        self.alias = alias
        self.private_key = private_key
        self.addr = account.address_from_private_key(private_key)


def fund_to_min(alias: str, target_addr: str, micro_algos: int) -> None:
    print(
        "Funding {} with address {} => {} Algos (if needed)".format(
            alias, target_addr, micro_algos / 1_000_000
        )
    )
    algo_setup.dev_fund_to_min(target_addr, micro_algos / 1_000_000)
    print(f"{alias} balance = {algo_utils.algos(target_addr)} Algos")


def fund(target_account: Account, micro_algos: int) -> None:
    fund_to_min(target_account.alias, target_account.addr, micro_algos)


def sign_and_send_txn(
    sender: Account, txn: transaction.Transaction
) -> algo_utils.PendingTxnResponse:
    signed_txn = txn.sign(sender.private_key)
    sent_txn_id = algod_client.send_transaction(signed_txn)
    print(f"Successfully sent transaction with txID: {sent_txn_id}")
    response = algo_utils.wait_for_transaction(algod_client, signed_txn.get_txid())
    return response


def generate_create_tadeed_algo(
    terminal_asset_alias: str, multi: MultisigAccount, manager: Account
) -> transaction.MultisigTransaction:
    txn = transaction.AssetCreateTxn(
        sender=multi.address(),
        total=1,
        decimals=0,
        default_frozen=False,
        manager=manager.addr,
        asset_name=terminal_asset_alias,
        unit_name="TADEED",
        sp=sp,
    )
    return multi.create_mtx(txn)


################
# Main demo code
################
holly: Account = Account("Holly", algo_setup.DEV_DEMO_HOLLY_SK)
daemon: Account = Account(
    "Smart Daemon", holly_ta_daemon_settings.sk.get_secret_value()
)
gnf_admin: Account = Account("GNF Admin", gnf_settings.admin_acct_sk.get_secret_value())

multi: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, daemon.addr, holly.addr],
)

# Funding
fund(holly, FUNDING_AMOUNT)
fund(daemon, FUNDING_AMOUNT)
fund(gnf_admin, FUNDING_AMOUNT)
fund_to_min("Join Account", multi.addr, FUNDING_AMOUNT)
print("===")

# Creating a new deed
ta_deed_mtx: MultisigTransaction = generate_create_tadeed_algo(
    DEED_ALIAS, multi, daemon
)
ta_deed_mtx.sign(daemon.private_key)

# Try to make a CreateTadeedAlgo message as the daemon to send to the GNodeFactory for
# it to co-sign. The Schema enforces a lot of axioms (see schemata/create_ta_deed.py)

try:
    payload = CreateTadeedAlgo_Maker(
        validator_addr=daemon.addr,
        half_signed_deed_creation_mtx=encoding.msgpack_encode(ta_deed_mtx),
    ).tuple
except SchemaError as e:
    print(e)

print("===")
"""
Errors making create.tavalidatorcert.algo.010:
    - Axiom 3: The MultiSig must be the 2-sig multi[Gnf Admin, payload.ValidatorAddr].
        Got ..72R4HM.
        Expected ..NEZ37A
    - Manager must be GnfAdmin ..4G5ALI, got ..AL62EA.
    - The asset name must have valid GNode format: words seperated by dots must be alphanumeric.
        Got 'My Deed just for demo'
    - The asset name must be a potential GNodeAlias in a dev universe.
        words seperated by dots must be alphanumeric. Got 'My Deed just for demo'
"""

# The schema checking tries to provide as many errors as possible to fix. However,
# sometimes it will take a few iterations to resolve all the issues
multi_2: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, daemon.addr],
)
mtx_2: MultisigTransaction = generate_create_tadeed_algo(
    "My.deed.just.for.demo", multi_2, gnf_admin
)
mtx_2.sign(daemon.private_key)

try:
    payload = CreateTadeedAlgo_Maker(
        validator_addr=daemon.addr,
        half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx_2),
    ).tuple
except SchemaError as e:
    print(e)

print("===")
"""
Errors making create.tavalidatorcert.algo.010:
    - The asset name must have valid GNode format: alias must be lowercase. Got 'My.deed.just.for.demo'
    - The asset name must be a potential GNodeAlias in a dev universe. alias must be lowercase. Got 'My.deed.just.for.demo'
"""

multi_3: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, daemon.addr],
)
mtx_3: MultisigTransaction = generate_create_tadeed_algo(
    "my.deed.just.for.demo", multi_3, gnf_admin
)
mtx_3.sign(daemon.private_key)

try:
    payload = CreateTadeedAlgo_Maker(
        validator_addr=daemon.addr,
        half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx_3),
    ).tuple
except SchemaError as e:
    print(e)

print("===")
"""
Errors making create.tavalidatorcert.algo.010:
    - The asset name must be a potential GNodeAlias in a dev universe. World alias for dev universe must start with d. Got my
"""

multi_4: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, daemon.addr],
)
mtx_4: MultisigTransaction = generate_create_tadeed_algo(
    "dw.deed.just.for.demo.which.is.really.really.long", multi_4, gnf_admin
)
mtx_4.sign(daemon.private_key)

try:
    payload = CreateTadeedAlgo_Maker(
        validator_addr=daemon.addr,
        half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx_4),
    ).tuple
except SchemaError as e:
    print(e)

print("===")

"""
Errors making create.tavalidatorcert.algo.010:
    - asset name must be <= 32 char. Got 49
"""

multi_5: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, daemon.addr],
)
mtx_5: MultisigTransaction = generate_create_tadeed_algo(
    "dw.just.for.demo", multi_5, gnf_admin
)
mtx_5.sign(daemon.private_key)

payload = CreateTadeedAlgo_Maker(
    validator_addr=daemon.addr,
    half_signed_deed_creation_mtx=encoding.msgpack_encode(mtx_5),
).tuple

# THIS ONE PASSES. It then can ask the GNodeFactory to sign


gnf = GNodeFactoryDb(settings=config.GnfSettings())

gnf.create_tadeed_algo_received(payload)
