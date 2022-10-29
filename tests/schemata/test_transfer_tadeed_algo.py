"""Tests transfer.tadeed.algo.020 type"""
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
from schemata.transfer_tadeed_algo_maker import TransferTadeedAlgo_Maker as Maker


def make_new_ta_deed(
    client: AlgodClient,
    test_acct: algo_utils.BasicAccount,
    gnf_admin: algo_utils.BasicAccount,
) -> int:
    multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin.addr, test_acct.addr],
    )

    txn = transaction.AssetCreateTxn(
        sender=multi.address(),
        total=1,
        decimals=0,
        default_frozen=False,
        manager=gnf_admin.addr,
        asset_name="dw1.iso.test.ta",
        unit_name="TADEED",
        sp=client.suggested_params(),
    )

    mtx = multi.create_mtx(txn)
    mtx.sign(gnf_admin.sk)
    mtx.sign(test_acct.sk)
    response = algo_utils.send_signed_mtx(client=client, mtx=mtx)
    return response.asset_idx


def get_payload_mtx(
    client: AlgodClient,
    test_acct: algo_utils.BasicAccount,
    gnf_admin: algo_utils.BasicAccount,
    ta_multi_addr: str,
    ta_deed_idx: int,
) -> str:
    validator_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin.addr, test_acct.addr],
    )

    transferTxn = transaction.AssetTransferTxn(
        sender=validator_multi.addr,
        receiver=ta_multi_addr,
        amt=1,
        index=ta_deed_idx,
        sp=client.suggested_params(),
    )

    mtx = validator_multi.create_mtx(transferTxn)
    mtx.sign(test_acct.sk)
    return encoding.msgpack_encode(mtx)


def test_transfer_tadeed_algo_generated():
    client: AlgodClient = algo_utils.get_algod_client(config.Algo())
    test_acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
        "LZlZFgStdj2T0otiJTRezerJhys0isRu4e6AM6fJJCRT03r0ziZrA44MFjjh6i6V2ySSQyRiCwvVzthpxjV7xA=="
    )

    gnf_admin: algo_utils.BasicAccount = algo_utils.BasicAccount(
        config.GnfSettings().admin_acct_sk.get_secret_value()
    )
    test_ta_daemon: algo_utils.BasicAccount = algo_utils.BasicAccount(
        "MWiOzdkKWw3Ah8BIz1s7KBZzV+8/VrTAPBUOhnHE3ooOZIYyJbRTR8Pphsbhd2D+RszOpuGd8cPuAnDjVZ+LUQ=="
    )
    test_ta_owner: algo_utils.BasicAccount = algo_utils.BasicAccount(
        "U6pVpBafuVb+xvkNeUAnZlxr7xbUim9tOKCzKeCd+87Ro6GY6JxPOqv9mGIV6MRl+PqlNa85CEk5DLB1O0zK2g=="
    )

    ta_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[
            config.Algo().gnf_admin_addr,
            test_ta_daemon.addr,
            test_ta_owner.addr,
        ],
    )
    validator_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
        version=1,
        threshold=2,
        addresses=[gnf_admin.addr, test_acct.addr],
    )
    min_algos = config.Algo().ta_deed_consideration_algos
    dev_utils.algo_setup.dev_fund_to_min(ta_multi.addr, min_algos)
    dev_utils.algo_setup.dev_fund_to_min(validator_multi.addr, 1)
    dev_utils.algo_setup.dev_fund_to_min(test_acct.addr, 1)
    ta_deed_idx = make_new_ta_deed(client, test_acct, gnf_admin)

    opt_in_txn = transaction.AssetOptInTxn(
        sender=ta_multi.addr,
        index=ta_deed_idx,
        sp=client.suggested_params(),
    )
    opt_in_mtx = ta_multi.create_mtx(opt_in_txn)
    opt_in_mtx.sign(gnf_admin.sk)
    opt_in_mtx.sign(test_ta_daemon.sk)
    algo_utils.send_signed_mtx(client, opt_in_mtx)

    mtx = get_payload_mtx(
        client=client,
        test_acct=test_acct,
        gnf_admin=gnf_admin,
        ta_multi_addr=ta_multi.addr,
        ta_deed_idx=ta_deed_idx,
    )

    gw_dict = {
        "FirstDeedTransferMtx": mtx,
        "DeedValidatorAddr": test_acct.addr,
        "TaOwnerAddr": test_ta_owner.addr,
        "TaDaemonAddr": test_ta_daemon.addr,
        "MicroLat": 44838681,
        "MicroLon": -68705311,
        "TypeName": "transfer.tadeed.algo.020",
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
        first_deed_transfer_mtx=gw_tuple.FirstDeedTransferMtx,
        deed_validator_addr=gw_tuple.DeedValidatorAddr,
        ta_daemon_addr=gw_tuple.TaDaemonAddr,
        ta_owner_addr=gw_tuple.TaOwnerAddr,
        micro_lat=gw_tuple.MicroLat,
        micro_lon=gw_tuple.MicroLon,
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

    orig_value = gw_dict["FirstDeedTransferMtx"]
    del gw_dict["FirstDeedTransferMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FirstDeedTransferMtx"] = orig_value

    orig_value = gw_dict["DeedValidatorAddr"]
    del gw_dict["DeedValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DeedValidatorAddr"] = orig_value

    orig_value = gw_dict["TaDaemonAddr"]
    del gw_dict["TaDaemonAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaDaemonAddr"] = orig_value

    orig_value = gw_dict["TaOwnerAddr"]
    del gw_dict["TaOwnerAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaOwnerAddr"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["FirstDeedTransferMtx"]
    gw_dict["FirstDeedTransferMtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FirstDeedTransferMtx"] = orig_value

    orig_value = gw_dict["DeedValidatorAddr"]
    gw_dict["DeedValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DeedValidatorAddr"] = orig_value

    orig_value = gw_dict["TaDaemonAddr"]
    gw_dict["TaDaemonAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaDaemonAddr"] = orig_value

    orig_value = gw_dict["TaOwnerAddr"]
    gw_dict["TaOwnerAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaOwnerAddr"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "transfer.tadeed.algo.020"
