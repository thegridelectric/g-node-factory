"""Tests optin.tadeed.algo type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import OptinTadeedAlgo_Maker as Maker


# def test_optin_tadeed_algo_generated():


#     d = {
#         "TaDaemonAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "ValidatorAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         "NewDeedOptInMtx": 'gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCD8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBqFzxEAEp8UcTEJSyTmgw96/mCnNHKfhkdYMCD5jxWejHRmPCrR8U9z/FBVsoCGbjDTTk2L1k7n/eVlumEk/M1KSe48Jo3RocgKhdgGjdHhuiaRhcGFyhaJhbq9Nb2xseSBNZXRlcm1haWSiYXXZKWh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9tb2xseWNvL3doby13ZS1hcmUvoW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdlGjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQQ5pG5vdGXEK01vbGx5IEluYyBUZWxlbWV0cnkgU3VydmV5b3JzIGFuZCBQdXJ2ZXlvcnOjc25kxCDHZxhdCT2TxxxZlZ/H5mIku1s4ulDm3EmU6dYKXCWEB6R0eXBlpGFjZmc=',
#         "TypeName": "optin.tadeed.algo",
#         "Version": "000",
#     }

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
#         ta_daemon_addr=gtuple.TaDaemonAddr,
#         ta_owner_addr=gtuple.TaOwnerAddr,
#         validator_addr=gtuple.ValidatorAddr,
#         new_deed_opt_in_mtx=gtuple.NewDeedOptInMtx,

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
#     del d2["TaDaemonAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["TaOwnerAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["ValidatorAddr"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["NewDeedOptInMtx"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     ######################################
#     # Behavior on incorrect types
#     ######################################

#     ######################################
#     # SchemaError raised if TypeName is incorrect
#     ######################################

#     d2 = dict(d, TypeName="not the type alias")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)
