"""Tests tavalidatorcert.algo.transfer type, version 000"""
import json
from typing import Dict

import dotenv
import pytest
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient
from pydantic import ValidationError

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.dev_utils.algo_setup as algo_setup
from gnf.errors import SchemaError
from gnf.schemata import TavalidatorcertAlgoTransfer_Maker as Maker


def make_new_test_cert_and_return_asset_idx(
    client: AlgodClient,
    test_acct: algo_utils.BasicAccount,
    gnf_admin: algo_utils.BasicAccount,
) -> int:
    multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin.addr, test_acct.addr],
    )
    if algo_utils.algos(multi.addr) is None:
        algo_setup.dev_fund_account(
            config.VanillaSettings(_env_file=dotenv.find_dotenv()),
            to_addr=test_acct.addr,
            amt_in_micros=1_000_000,
        )
        algo_setup.dev_fund_account(
            config.VanillaSettings(_env_file=dotenv.find_dotenv()),
            to_addr=multi.addr,
            amt_in_micros=config.GnfPublic().gnf_validator_funding_threshold_algos
            * 10**6,
        )
    elif algo_utils.algos(multi.addr) < 100:
        algo_setup.dev_fund_account(
            config.VanillaSettings(_env_file=dotenv.find_dotenv()),
            to_addr=test_acct.addr,
            amt_in_micros=1_000_000,
        )
        algo_setup.dev_fund_account(
            config.VanillaSettings(_env_file=dotenv.find_dotenv()),
            to_addr=multi.addr,
            amt_in_micros=config.GnfPublic().gnf_validator_funding_threshold_algos
            * 10**6,
        )

    txn = transaction.AssetCreateTxn(
        sender=multi.address(),
        total=1,
        decimals=0,
        default_frozen=False,
        manager=gnf_admin.addr,
        asset_name="Test Validator of nothingness",
        unit_name="VLDTR",
        note="witty note",
        url="http://localhost:5000/testValidator/who-we-are/",
        sp=client.suggested_params(),
    )

    mtx = multi.create_mtx(txn)
    mtx.sign(gnf_admin.sk)
    mtx.sign(test_acct.sk)
    response = algo_utils.send_signed_mtx(client=client, mtx=mtx)
    return response.asset_idx


def get_test_half_signed_cert_transfer_mtx(
    client: AlgodClient,
    test_acct: algo_utils.BasicAccount,
    gnf_admin: algo_utils.BasicAccount,
    asset_idx: int,
) -> str:
    multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin.addr, test_acct.addr],
    )

    optInTxn = transaction.AssetOptInTxn(
        sender=test_acct.addr,
        index=asset_idx,
        sp=client.suggested_params(),
    )
    signedTxn = optInTxn.sign(test_acct.sk)
    client.send_transaction(signedTxn)
    algo_utils.wait_for_transaction(client, signedTxn.get_txid())
    transferTxn = transaction.AssetTransferTxn(
        sender=multi.addr,
        receiver=test_acct.addr,
        amt=1,
        index=asset_idx,
        sp=client.suggested_params(),
    )

    mtx = multi.create_mtx(transferTxn)
    mtx.sign(test_acct.sk)
    return encoding.msgpack_encode(mtx)


def get_test_dict() -> Dict:
    settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
    client: AlgodClient = AlgodClient(
        settings.algo_api_secrets.algod_token.get_secret_value(),
        settings.public.algod_address,
    )
    test_acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
        "LZlZFgStdj2T0otiJTRezerJhys0isRu4e6AM6fJJCRT03r0ziZrA44MFjjh6i6V2ySSQyRiCwvVzthpxjV7xA=="
    )
    gnf_admin: algo_utils.BasicAccount = algo_utils.BasicAccount(
        config.GnfSettings(
            _env_file=dotenv.find_dotenv()
        ).admin_acct_sk.get_secret_value()
    )

    asset_idx = api_utils.get_validator_cert_idx(test_acct.addr)
    if asset_idx is None:
        asset_idx = make_new_test_cert_and_return_asset_idx(
            client, test_acct, gnf_admin
        )

    testHalfSignedCertTransferMtx = get_test_half_signed_cert_transfer_mtx(
        client, test_acct, gnf_admin, asset_idx
    )

    return {
        "ValidatorAddr": test_acct.addr,
        "HalfSignedCertTransferMtx": testHalfSignedCertTransferMtx,
        "TypeName": "tavalidatorcert.algo.transfer",
        "Version": "000",
    }


@pytest.mark.skip(reason="Skipped so a package can be published")
def test_tavalidatorcert_algo_transfer():
    d = get_test_dict()

    with pytest.raises(SchemaError):
        Maker.type_to_tuple(d)

    with pytest.raises(SchemaError):
        Maker.type_to_tuple('"not a dict"')

    # Test type_to_tuple
    gtype = json.dumps(d)
    gtuple = Maker.type_to_tuple(gtype)

    # test type_to_tuple and tuple_to_type maps
    assert Maker.type_to_tuple(Maker.tuple_to_type(gtuple)) == gtuple

    # test Maker init
    t = Maker(
        validator_addr=gtuple.ValidatorAddr,
        half_signed_cert_transfer_mtx=gtuple.HalfSignedCertTransferMtx,
    ).tuple
    assert t == gtuple

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    d2 = dict(d)
    del d2["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["HalfSignedCertTransferMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)
