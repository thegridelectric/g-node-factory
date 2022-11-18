from account import Account
from operations import (
    create_app,
    setup_app_opt_in,
    target_opt_in,
    transfer_deed_to_app,
    transfer_deed_to_dest,
    get_application_address
)
from resources import (
    getTemporaryAccount,
    createDummyAsset,
)
from setup import getAlgodClient
from util import (
    getBalances,
)


def print_balance(app_id: int, creator: Account, src: Account, dest: Account, debug: bool = False) -> None:
    creator_balance = getBalances(client, creator.getAddress())
    print("===============================================")
    src_balance = getBalances(client, src.getAddress())
    print("Creator account's balance", creator_balance, creator.getAddress() if debug else "")
    print("Smart contract with id=", app_id)

    app_address = get_application_address(app_id)
    app_balance = getBalances(client, app_address)
    dest_balance = getBalances(client, dest.getAddress())
    print(".Escrow account's balance", app_balance, app_address if debug else "")
    print(".Deed Owner account's balance", src_balance, src.getAddress() if debug else "")
    print(".(GNodeFactory) Target account's balance", dest_balance, dest.getAddress() if debug else "")
    print("===============================================")
    input("Press enter to continue")
    print("Next step...")


print("Demo start...")

client = getAlgodClient()
creator: Account = getTemporaryAccount(client)
owner: Account = getTemporaryAccount(client)
target: Account = getTemporaryAccount(client)

deed_amount = 1
deed_id = createDummyAsset(client, deed_amount, owner)
print("A demo deed created, id=", deed_id)

# Interact with smart contract here
app_id = create_app(client, target, creator, owner, deed_id)
app_address = get_application_address(app_id)

print_balance(app_id, creator, owner, target)

print("Setup (Contract Opt In)")
setup_app_opt_in(client, app_id, creator, deed_id)
print_balance(app_id, creator, owner, target)

print("Target Opt in")
target_opt_in(client, deed_id, target)
print_balance(app_id, creator, owner, target)

print("transfer deed -> smart contract")
transfer_deed_to_app(client, app_address, owner, deed_id, deed_amount)
print_balance(app_id, creator, owner, target)

print("transfer deed -> target")
transfer_deed_to_dest(client, app_id, creator, owner, target, deed_id)
print_balance(app_id, creator, owner, target)

print("Done.")

