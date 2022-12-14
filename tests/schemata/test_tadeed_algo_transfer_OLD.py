# """Tests tadeed.algo.transfer type, version 000"""
# import json
# from typing import Dict

# import pytest
# from algosdk import encoding
# from algosdk.future import transaction
# from algosdk.v2client.algod import AlgodClient
# from pydantic import ValidationError

# import gnf.algo_utils as algo_utils
# import gnf.config as config
# import gnf.dev_utils.algo_setup as algo_setup
# from gnf.errors import SchemaError
# from gnf.schemata import TadeedAlgoTransfer_Maker as Maker


# def make_new_ta_deed(
#     client: AlgodClient,
#     test_acct: algo_utils.BasicAccount,
#     gnf_admin: algo_utils.BasicAccount,
# ) -> int:
#     multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
#         version=1,
#         threshold=2,
#         addresses=[gnf_admin.addr, test_acct.addr],
#     )

#     txn = transaction.AssetCreateTxn(
#         sender=multi.address(),
#         total=1,
#         decimals=0,
#         default_frozen=False,
#         manager=gnf_admin.addr,
#         asset_name="d1.iso.test.ta",
#         unit_name="TADEED",
#         sp=client.suggested_params(),
#     )

#     mtx = multi.create_mtx(txn)
#     mtx.sign(gnf_admin.sk)
#     mtx.sign(test_acct.sk)
#     response = algo_utils.send_signed_mtx(client=client, mtx=mtx)
#     return response.asset_idx


# def get_payload_mtx(
#     client: AlgodClient,
#     test_acct: algo_utils.BasicAccount,
#     gnf_admin: algo_utils.BasicAccount,
#     ta_multi_addr: str,
#     ta_deed_idx: int,
# ) -> str:
#     validator_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
#         version=1,
#         threshold=2,
#         addresses=[gnf_admin.addr, test_acct.addr],
#     )

#     transferTxn = transaction.AssetTransferTxn(
#         sender=validator_multi.addr,
#         receiver=ta_multi_addr,
#         amt=1,
#         index=ta_deed_idx,
#         sp=client.suggested_params(),
#     )

#     mtx = validator_multi.create_mtx(transferTxn)
#     mtx.sign(test_acct.sk)
#     return encoding.msgpack_encode(mtx)


# def get_sample_dict() -> Dict:
# settings = config.BlahBlahBlahSettings()
# client: AlgodClient = AlgodClient(
#         settings.algo_api_secrets.algod_token.get_secret_value(),
#         settings.public.algod_address
#     )
#     test_acct: algo_utils.BasicAccount = algo_utils.BasicAccount(
#         "LZlZFgStdj2T0otiJTRezerJhys0isRu4e6AM6fJJCRT03r0ziZrA44MFjjh6i6V2ySSQyRiCwvVzthpxjV7xA=="
#     )

#     gnf_admin: algo_utils.BasicAccount = algo_utils.BasicAccount(
#         config.GnfSettings().admin_acct_sk.get_secret_value()
#     )
#     test_ta_daemon: algo_utils.BasicAccount = algo_utils.BasicAccount(
#         "MWiOzdkKWw3Ah8BIz1s7KBZzV+8/VrTAPBUOhnHE3ooOZIYyJbRTR8Pphsbhd2D+RszOpuGd8cPuAnDjVZ+LUQ=="
#     )
#     test_ta_owner: algo_utils.BasicAccount = algo_utils.BasicAccount(
#         "U6pVpBafuVb+xvkNeUAnZlxr7xbUim9tOKCzKeCd+87Ro6GY6JxPOqv9mGIV6MRl+PqlNa85CEk5DLB1O0zK2g=="
#     )
#     ta_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
#         version=1,
#         threshold=2,
#         addresses=[
#             config.Algo().gnf_admin_addr,
#             test_ta_daemon.addr,
#             test_ta_owner.addr,
#         ],
#     )
#     validator_multi: algo_utils.MultisigAccount = algo_utils.MultisigAccount(
#         version=1,
#         threshold=2,
#         addresses=[gnf_admin.addr, test_acct.addr],
#     )
#     min_algos = config.Algo().ta_deed_consideration_algos
#     algo_setup.dev_fund_to_min(ta_multi.addr, min_algos)
#     algo_setup.dev_fund_to_min(validator_multi.addr, 1)
#     algo_setup.dev_fund_to_min(test_acct.addr, 1)
#     ta_deed_idx = make_new_ta_deed(client, test_acct, gnf_admin)

#     opt_in_txn = transaction.AssetOptInTxn(
#         sender=ta_multi.addr,
#         index=ta_deed_idx,
#         sp=client.suggested_params(),
#     )
#     opt_in_mtx = ta_multi.create_mtx(opt_in_txn)
#     opt_in_mtx.sign(gnf_admin.sk)
#     opt_in_mtx.sign(test_ta_daemon.sk)
#     algo_utils.send_signed_mtx(client, opt_in_mtx)

#     mtx = get_payload_mtx(
#         client=client,
#         test_acct=test_acct,
#         gnf_admin=gnf_admin,
#         ta_multi_addr=ta_multi.addr,
#         ta_deed_idx=ta_deed_idx,
#     )

#     return {
#         "FirstDeedTransferMtx": mtx,
#         "DeedValidatorAddr": test_acct.addr,
#         "TaOwnerAddr": test_ta_owner.addr,
#         "TaDaemonAddr": test_ta_daemon.addr,
#         "MicroLat": 44838681,
#         "MicroLon": -68705311,
#         "TypeName": "tadeed.algo.transfer",
#         "Version": "000",
#     }


# def test_tadeed_algo_transfer():
#     d = get_sample_dict()

#     with pytest.raises(SchemaError):
#         Maker.type_to_tuple(d)

#     with pytest.raises(SchemaError):
#         Maker.type_to_tuple('"not a dict"')

#     # Test type_to_tuple
#     gtype = json.dumps(d)
#     gtuple = Maker.type_to_tuple(gtype)

#     # test type_to_tuple and tuple_to_type maps
#     assert Maker.type_to_tuple(Maker.tuple_to_type(gtuple)) == gtuple

#     # test Maker init
#     t = Maker(
#         first_deed_transfer_mtx=gtuple.FirstDeedTransferMtx,
#         micro_lat=gtuple.MicroLat,
#         deed_validator_addr=gtuple.DeedValidatorAddr,
#         ta_daemon_addr=gtuple.TaDaemonAddr,
#         ta_owner_addr=gtuple.TaOwnerAddr,
#         micro_lon=gtuple.MicroLon,
#     ).tuple
#     assert t == gtuple

#     ######################################
#     # SchemaError raised if missing a required attribute
#     ######################################

#     d2 = dict(d)
#     del d2["TypeName"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["FirstDeedTransferMtx"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["MicroLat"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["DeedValidatorAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["TaDaemonAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["TaOwnerAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["MicroLon"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     ######################################
#     # Behavior on incorrect types
#     ######################################

#     d2 = dict(d, MicroLat="'44838681'.1")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d, MicroLon="'-68705311'.1")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)

#     ######################################
#     # SchemaError raised if TypeName is incorrect
#     ######################################

#     d2 = dict(d, TypeName="not the type alias")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)
