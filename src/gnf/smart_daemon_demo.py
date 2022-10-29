from typing import Optional

import algo_utils
import config
from algo_utils import MultisigAccount
from algosdk import account
from algosdk.future import transaction
from algosdk.future.transaction import MultisigTransaction
from algosdk.v2client.algod import AlgodClient
from config import Algo
from config import GnfSettings
from config import HollyTaDaemonSettings
from dev_utils import algo_setup
from dev_utils.algo_setup import FUNDING_AMOUNT
from g_node_factory_db import GNodeFactoryDb
from schemata.create_tadeed_algo import CreateTadeedAlgo


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
        introduce(self.alias, self.addr)


def introduce(alias: str, addr: str) -> None:
    print(f"Account {alias} with address {addr}")


def fund_amount(alias: str, target_addr: str, micro_algos: int) -> None:
    print(
        "Funding {} with address {} => {} Algos".format(
            alias, target_addr, micro_algos / 1_000_000
        )
    )
    algo_setup.dev_fund_account(algo_settings, target_addr, micro_algos)
    print(f"{alias} balance = {algo_utils.algos(target_addr)} Algos")


def fund(target_account: Account, micro_algos: int) -> None:
    fund_amount(target_account.alias, target_account.addr, micro_algos)


def sign_and_send_txn(
    sender: Account, txn: transaction.Transaction
) -> algo_utils.PendingTxnResponse:
    signed_txn = txn.sign(sender.private_key)
    sent_txn_id = algod_client.send_transaction(signed_txn)
    print(f"Successfully sent transaction with txID: {sent_txn_id}")
    response = algo_utils.wait_for_transaction(algod_client, signed_txn.get_txid())
    return response


def generate_create_tadeed_algo(
    terminal_asset_alias: str, mutli: MultisigAccount, manager: Account
) -> transaction.MultisigTransaction:
    txn = transaction.AssetCreateTxn(
        sender=mutli.address(),
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
smart_daemon_validator: Account = Account(
    "Smart Daemon (Validator)", holly_ta_daemon_settings.sk.get_secret_value()
)
gnf_admin: Account = Account("GNF Admin", gnf_settings.admin_acct_sk.get_secret_value())
gnf_db: GNodeFactoryDb = GNodeFactoryDb(settings=gnf_settings)

multi: MultisigAccount = algo_utils.MultisigAccount(
    version=1,
    threshold=2,
    addresses=[gnf_admin.addr, smart_daemon_validator.addr, holly.addr],
)
introduce("Joint Account", multi.address())

# Funding
fund(holly, FUNDING_AMOUNT)
fund(smart_daemon_validator, FUNDING_AMOUNT)
fund(gnf_admin, FUNDING_AMOUNT)
fund_amount("Join Account", multi.addr, FUNDING_AMOUNT)
print("===")

# Creating a new deed
ta_deed_mtx: MultisigTransaction = generate_create_tadeed_algo(
    DEED_ALIAS, multi, smart_daemon_validator
)

# To create we need at least 2 signatures
ta_deed_mtx.sign(smart_daemon_validator.private_key)

# It looks like:
# - in this demo we don't want to directly sign it by GNF here.
# - we sign it indirectly via sending CreateTadeedAlgo to GNodeFactoryDb
# - GNodeFactoryDb will send it to Blockchain and wait until it's completed
#
# Old version:
# ta_deed_mtx.sign(gnf_admin.private_key)
# sent_txn_id: str = algod_client.send_transaction(ta_deed_mtx)
# response = algo_utils.wait_for_transaction(algod_client, sent_txn_id)
# print("Asset created, asset_idx={}".format(response.asset_idx))

create_ta_deed_algo: CreateTadeedAlgo = CreateTadeedAlgo(
    ValidatorAddr=smart_daemon_validator.addr, HalfSignedDeedCreationMtx=ta_deed_mtx
)
asset_id: Optional[int] = gnf_db.create_tadeed_algo_received(create_ta_deed_algo)
print(f"Asset created with id={asset_id}" if asset_id else "Asset not created")

# At this point we should have a Deed signed by
# - the validator (smart daemon) and
# - Gnf Admin
#

# The next steps is to create Smart Contract
# Logic for the Smart Contract: TBD
