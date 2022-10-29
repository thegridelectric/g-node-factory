"""Tests signandsubmit.mtx.algo.000 type"""
import json

import pytest
from errors import SchemaError
from schemata.signandsubmit_mtx_algo_maker import SignandsubmitMtxAlgo_Maker as Maker


# def test_signandsubmit_mtx_algo_generated():

#     gw_dict = {
#         "SignerAddress": "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
#         "Mtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCCaszbRc+Y8G+clVkPcnrpfOvDkLUKVB3r+nOM5G4mCaqFzxEAYjou1knNqJfnQ/Hf+9BR5Q3iODO9lLK/k3raQokAGxcmoNYXJvONGUllxbsX2LgdkdA+Zl1C7s8MRKTK1DHQKo3RocgKhdgGjdHhuiKRhcGFyhaJhbq5UZXN0IFZhbGlkYXRvcqJhdbZodHRwOi8vcmFuZG9tLndlYi5wYWdloW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdhKjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQP6o3NuZMQgvbASYXCX0pGddnnNoDyK5A6U3tG4JMsc+ZNdSRlcSzykdHlwZaRhY2Zn",
#         "Addresses": [
#             "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI",
#             "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
#             "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         ],
#         "Threshold": 2,
#         "TypeName": "signandsubmit.mtx.algo.000",
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
#         signer_address=gw_tuple.SignerAddress,
#         mtx=gw_tuple.Mtx,
#         addresses=gw_tuple.Addresses,
#         threshold=gw_tuple.Threshold,
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

#     orig_value = gw_dict["SignerAddress"]
#     del gw_dict["SignerAddress"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["SignerAddress"] = orig_value

#     orig_value = gw_dict["Mtx"]
#     del gw_dict["Mtx"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Mtx"] = orig_value

#     orig_value = gw_dict["Addresses"]
#     del gw_dict["Addresses"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Addresses"] = orig_value

#     orig_value = gw_dict["Threshold"]
#     del gw_dict["Threshold"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Threshold"] = orig_value

#     ######################################
#     # SchemaError raised if attributes have incorrect type
#     ######################################

#     orig_value = gw_dict["SignerAddress"]
#     gw_dict["SignerAddress"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["SignerAddress"] = orig_value

#     orig_value = gw_dict["Mtx"]
#     gw_dict["Mtx"] = 42
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Mtx"] = orig_value

#     orig_value = gw_dict["Addresses"]
#     gw_dict["Addresses"] = "This string is not a list."
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Addresses"] = [42]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Addresses"] = orig_value

#     orig_value = gw_dict["Threshold"]
#     gw_dict["Threshold"] = 1.1
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["Threshold"] = orig_value

#     ######################################
#     # SchemaError raised if TypeName is incorrect
#     ######################################

#     gw_dict["TypeName"] = "not the type alias"
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(gw_dict)
#     gw_dict["TypeName"] = "signandsubmit.mtx.algo.000"
