from typing import Tuple

from algosdk import encoding
from algosdk.future import transaction
from algosdk.logic import get_application_address
from algosdk.v2client.algod import AlgodClient

from account import Account
from contracts import approval_program, clear_state_program
from util import (
    waitForTransaction,
    fullyCompileContract, getAppGlobalState,
)


def compile_contract(client: AlgodClient) -> Tuple[bytes, bytes]:
    approval_compiled = fullyCompileContract(client, approval_program())
    clear_compiled = fullyCompileContract(client, clear_state_program())

    return approval_compiled, clear_compiled


def create_app(
        client: AlgodClient,
        target: Account,
        creator: Account,
        owner: Account,
        deed_id: int
) -> int:
    approval, clear = compile_contract(client)

    global_schema = transaction.StateSchema(num_uints=1, num_byte_slices=3)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_args = [
        encoding.decode_address(target.getAddress()),
        encoding.decode_address(creator.getAddress()),
        encoding.decode_address(owner.getAddress()),
        deed_id.to_bytes(8, "big"),
    ]

    app_txn = transaction.ApplicationCreateTxn(
        sender=creator.getAddress(),
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=global_schema,
        local_schema=local_schema,
        app_args=app_args,
        sp=client.suggested_params()
    )

    signed = app_txn.sign(creator.getPrivateKey())
    client.send_transaction(signed)
    response = waitForTransaction(client, signed.get_txid())

    return response.applicationIndex


def setup_app_opt_in(
        client: AlgodClient,
        app_id: int,
        creator: Account,
        deed_id: int,
) -> None:
    suggested_params = client.suggested_params()
    funding_amount = 203_000
    app_addr = get_application_address(app_id)

    fund_txn = transaction.PaymentTxn(
        sender=creator.getAddress(),
        receiver=app_addr,
        amt=funding_amount,
        sp=suggested_params
    )

    app_setup_txn = transaction.ApplicationCallTxn(
        sender=creator.getAddress(),
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[b"setup"],
        foreign_assets=[deed_id],
        sp=suggested_params
    )

    transaction.assign_group_id([fund_txn, app_setup_txn])

    signed_fund_txn = fund_txn.sign(creator.getPrivateKey())
    signed_setup_txn = app_setup_txn.sign(creator.getPrivateKey())
    client.send_transactions([signed_fund_txn, signed_setup_txn])
    waitForTransaction(client, signed_fund_txn.get_txid())


def target_opt_in(
        client: AlgodClient,
        deed_id: int,
        account: Account
) -> None:
    suggested_params = client.suggested_params()

    txn = transaction.AssetOptInTxn(
        sender=account.getAddress(),
        index=deed_id,
        sp=suggested_params
    )

    signed = txn.sign(account.getPrivateKey())
    client.send_transaction(signed)
    waitForTransaction(client, signed.get_txid())


def transfer_deed_to_app(
        client: AlgodClient,
        app_account_addr: str,
        deed_holder: Account,
        deed_id: int,
        nft_amount: int
) -> None:
    suggested_params = client.suggested_params()

    deed_from_holder_to_app_txn = transaction.AssetTransferTxn(
        sender=deed_holder.getAddress(),
        receiver=app_account_addr,
        index=deed_id,
        amt=nft_amount,
        sp=suggested_params
    )

    signed_txn1 = deed_from_holder_to_app_txn.sign(deed_holder.getPrivateKey())

    client.send_transaction(signed_txn1)
    waitForTransaction(client, signed_txn1.get_txid())


def transfer_deed_to_dest(
        client: AlgodClient,
        app_id: int,
        creator: Account,
        owner: Account,
        target: Account,
        deed_id: int,
) -> None:
    suggested_params = client.suggested_params()

    accounts = [target.getAddress()]
    appGlobalState = getAppGlobalState(client, app_id)

    deed_from_app_to_target_txn = transaction.ApplicationCallTxn(
        sender=target.getAddress(),
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[b"transfer"],
        foreign_assets=[deed_id],
        accounts=accounts,
        sp=suggested_params
    )

    signed_txn2 = deed_from_app_to_target_txn.sign(target.getPrivateKey())
    client.send_transaction(signed_txn2)
    waitForTransaction(client, signed_txn2.get_txid())
