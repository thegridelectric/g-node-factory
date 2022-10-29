"""Tests transfer.validatorcert.algo.010 type"""
import json

import algo_utils
import api_utils
import config
import dev_utils.algo_setup
import pytest
from algosdk import encoding
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient
from errors import SchemaError
from g_node_factory_db import GNodeFactoryDb
from schemata.transfer_tavalidatorcert_algo_maker import (
    TransferTavalidatorcertAlgo_Maker as Maker,
)


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
        dev_utils.algo_setup.dev_fund_account(
            config.Algo(), to_addr=test_acct.addr, amt_in_micros=1_000_000
        )
        dev_utils.algo_setup.dev_fund_account(
            config.Algo(),
            to_addr=multi.addr,
            amt_in_micros=config.Algo().gnf_validator_funding_threshold_algos * 10**6,
        )
    elif algo_utils.algos(multi.addr) < 100:
        dev_utils.algo_setup.dev_fund_account(
            config.Algo(), to_addr=test_acct.addr, amt_in_micros=1_000_000
        )
        dev_utils.algo_setup.dev_fund_account(
            config.Algo(),
            to_addr=multi.addr,
            amt_in_micros=config.Algo().gnf_validator_funding_threshold_algos * 10**6,
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


def test_transfer_validatorcert_algo():
    client: AlgodClient = algo_utils.get_algod_client(config.Algo())
    test_acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
        "LZlZFgStdj2T0otiJTRezerJhys0isRu4e6AM6fJJCRT03r0ziZrA44MFjjh6i6V2ySSQyRiCwvVzthpxjV7xA=="
    )
    gnf_admin: algo_utils.BasicAccount = algo_utils.BasicAccount(
        config.GnfSettings().admin_acct_sk.get_secret_value()
    )

    asset_idx = api_utils.get_validator_cert_idx(test_acct.addr)
    if asset_idx is None:
        asset_idx = make_new_test_cert_and_return_asset_idx(
            client, test_acct, gnf_admin
        )

    testHalfSignedCertTransferMtx = get_test_half_signed_cert_transfer_mtx(
        client, test_acct, gnf_admin, asset_idx
    )

    gw_dict = {
        "ValidatorAddr": test_acct.addr,
        "HalfSignedCertTransferMtx": testHalfSignedCertTransferMtx,
        "TypeName": "transfer.tavalidatorcert.algo.010",
    }

    with pytest.raises(SchemaError):
        Maker.type_to_tuple(gw_dict)

    with pytest.raises(SchemaError):
        Maker.type_to_tuple('"not a dict"')

    # Test type_to_tuple
    gw_type = json.dumps(gw_dict)
    gw_tuple = Maker.type_to_tuple(gw_type)

    # test type_to_tuple and tuple_to_type maps
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple

    # test Maker init
    t = Maker(
        validator_addr=gw_tuple.ValidatorAddr,
        half_signed_cert_transfer_mtx=gw_tuple.HalfSignedCertTransferMtx,
        #
    ).tuple
    assert t == gw_tuple

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    orig_value = gw_dict["TypeName"]
    del gw_dict["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = orig_value

    orig_value = gw_dict["ValidatorAddr"]
    del gw_dict["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["HalfSignedCertTransferMtx"]
    del gw_dict["HalfSignedCertTransferMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedCertTransferMtx"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["ValidatorAddr"]
    gw_dict["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["HalfSignedCertTransferMtx"]
    gw_dict["HalfSignedCertTransferMtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedCertTransferMtx"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "transfer.validatorcert.algo.010"
