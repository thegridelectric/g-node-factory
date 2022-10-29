import algo_utils
import algosdk
import config
import dev_utils.algo_setup
import pytest
from errors import AlgoError


def test_pay_account():
    addr0: algo_utils.BasicAccount = dev_utils.algo_setup.get_gnf_admin_address()
    addr1: algo_utils.BasicAccount = dev_utils.algo_setup.get_molly_metermaid_address()
    addresses = [addr0, addr1]
    multi = algo_utils.MultisigAccount(version=1, threshold=2, addresses=addresses)

    initial_balance = algo_utils.micro_algos(multi.addr)
    # This is the test of payAccount working, called by devFundAccount which grabs
    # a genesis BasicAccount
    r = dev_utils.algo_setup.dev_fund_account(
        settings_algo=config.Algo(), to_addr=multi.addr, amt_in_micros=200_000
    )
    assert isinstance(r, algo_utils.PendingTxnResponse)
    assert algo_utils.micro_algos(multi.addr) >= initial_balance + 200_000

    client = algo_utils.get_algod_client(config.Algo())

    # MultisigAccount attempts to pay a BasicAccount. But a MultisigAccount does not
    # contain the private signing keys of its component addresses, so this will fail.

    with pytest.raises(AlgoError):
        algo_utils.pay_account(
            client=client, sender=multi, to_addr=addr1, amt_in_micros=100_000
        )


def test_basic_account():
    testAcct = algosdk.account.generate_account()

    acct: algo_utils.BasicAccount = algo_utils.BasicAccount(private_key=testAcct[0])

    assert acct.addr == testAcct[1]
    assert acct.sk == testAcct[0]

    acct: algo_utils.BasicAccount = algo_utils.BasicAccount()

    assert acct.addr == acct.address()
    assert acct.sk == acct.private_key()
    assert acct.address_as_bytes == algosdk.encoding.decode_address(acct.addr)
    assert acct.mnemonic == algosdk.mnemonic.from_private_key(acct.sk)
    assert acct.from_mnemonic(acct.mnemonic) == acct
    assert acct.__repr__() is not None
    assert acct.addr_short_hand == acct.addr[-6:]


def test_multisig_account():
    acct0: algo_utils.BasicAccount = algo_utils.BasicAccount()
    acct1: algo_utils.BasicAccount = algo_utils.BasicAccount()
    addresses = [acct0.addr, acct1.addr]

    with pytest.raises(Exception):
        m = algo_utils.MultisigAccount(
            version=1, threshold=0, addresses=["Hello", "World"]
        )
    with pytest.raises(algosdk.error.InvalidThresholdError):
        m = algo_utils.MultisigAccount(version=1, threshold=0, addresses=addresses)

    with pytest.raises(algosdk.error.InvalidThresholdError):
        m = algo_utils.MultisigAccount(version=1, threshold=3, addresses=addresses)

    multi = algo_utils.MultisigAccount(version=1, threshold=2, addresses=addresses)
    msig = algosdk.future.transaction.Multisig(
        version=1, threshold=2, addresses=addresses
    )

    assert multi.addresses == addresses

    acct2 = algo_utils.BasicAccount()
    addresses.append(acct2.addr)
    # multi grabs a copy of the list of addresses. If the original list changes,
    # multi keeps the original
    assert multi.addresses == [acct0.addr, acct1.addr]

    assert multi.address() == msig.address()

    assert multi.addr == multi.address()
    assert multi.addr_short_hand == multi.addr[-6:]

    subsig0: algosdk.future.transaction.MultisigSubsig = msig.subsigs[0]
    assert subsig0.public_key == acct0.address_as_bytes

    assert multi.__repr__() is not None