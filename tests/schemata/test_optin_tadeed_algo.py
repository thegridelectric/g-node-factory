"""Tests optin.tadeed.algo.001 type"""
import json

import pytest
from errors import SchemaError
from schemata.optin_tadeed_algo_maker import OptinTadeedAlgo_Maker as Maker


# def test_optin_tadeed_algo_generated():

#     gw_dict = {
#         "ValidatorAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "NewDeedOptInMtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCD8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBqFzxEAEp8UcTEJSyTmgw96/mCnNHKfhkdYMCD5jxWejHRmPCrR8U9z/FBVsoCGbjDTTk2L1k7n/eVlumEk/M1KSe48Jo3RocgKhdgGjdHhuiaRhcGFyhaJhbq9Nb2xseSBNZXRlcm1haWSiYXXZKWh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9tb2xseWNvL3doby13ZS1hcmUvoW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdlGjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQQ5pG5vdGXEK01vbGx5IEluYyBUZWxlbWV0cnkgU3VydmV5b3JzIGFuZCBQdXJ2ZXlvcnOjc25kxCDHZxhdCT2TxxxZlZ/H5mIku1s4ulDm3EmU6dYKXCWEB6R0eXBlpGFjZmc=",
#         "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "TaDaemonAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "TypeName": "optin.tadeed.algo.001",
#     }

#     with pytest.raises(SchemaError):
#         Maker.type_to_tuple(gw_dict)

#     with pytest.raises(SchemaError):
#         Maker.type_to_tuple('"not a dict"')

#     # Test type_to_tuple
#     gw_type = json.dumps(gw_dict)
#     gw_tuple = Maker.type_to_tuple(gw_type)

#     # test type_to_tuple and tuple_to_type maps
#     assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple

#     # test Maker init
#     t = Maker(
#         validator_addr=gw_tuple.ValidatorAddr,
#         new_deed_opt_in_mtx=gw_tuple.NewDeedOptInMtx,
#         ta_owner_addr=gw_tuple.TaOwnerAddr,
#         ta_daemon_addr=gw_tuple.TaDaemonAddr,
#         #
#     ).tuple
#     assert t == gw_tuple

#     ######################################
#     # SchemaError raised if missing a required attribute
#     ######################################

#     orig_value = gw_dict["TypeName"]
#     del gw_dict["TypeName"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TypeName"] = orig_value

#     orig_value = gw_dict["ValidatorAddr"]
#     del gw_dict["ValidatorAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["ValidatorAddr"] = orig_value

#     orig_value = gw_dict["NewDeedOptInMtx"]
#     del gw_dict["NewDeedOptInMtx"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["NewDeedOptInMtx"] = orig_value

#     orig_value = gw_dict["TaOwnerAddr"]
#     del gw_dict["TaOwnerAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TaOwnerAddr"] = orig_value

#     orig_value = gw_dict["TaDaemonAddr"]
#     del gw_dict["TaDaemonAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TaDaemonAddr"] = orig_value

#     ######################################
#     # SchemaError raised if attributes have incorrect type
#     ######################################

#     orig_value = gw_dict["ValidatorAddr"]
#     gw_dict["ValidatorAddr"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["ValidatorAddr"] = orig_value

#     orig_value = gw_dict["NewDeedOptInMtx"]
#     gw_dict["NewDeedOptInMtx"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["NewDeedOptInMtx"] = orig_value

#     orig_value = gw_dict["TaOwnerAddr"]
#     gw_dict["TaOwnerAddr"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TaOwnerAddr"] = orig_value

#     orig_value = gw_dict["TaDaemonAddr"]
#     gw_dict["TaDaemonAddr"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TaDaemonAddr"] = orig_value

#     ######################################
#     # SchemaError raised if TypeName is incorrect
#     ######################################

#     gw_dict["TypeName"] = "not the type alias"
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TypeName"] = "optin.tadeed.algo.001"
