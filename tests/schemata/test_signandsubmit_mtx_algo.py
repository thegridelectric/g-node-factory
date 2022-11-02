"""Tests signandsubmit.mtx.algo type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import SignandsubmitMtxAlgo_Maker as Maker


# def test_signandsubmit_mtx_algo_generated():

#     d = {
#         "Mtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCCaszbRc+Y8G+clVkPcnrpfOvDkLUKVB3r+nOM5G4mCaqFzxEAYjou1knNqJfnQ/Hf+9BR5Q3iODO9lLK/k3raQokAGxcmoNYXJvONGUllxbsX2LgdkdA+Zl1C7s8MRKTK1DHQKo3RocgKhdgGjdHhuiKRhcGFyhaJhbq5UZXN0IFZhbGlkYXRvcqJhdbZodHRwOi8vcmFuZG9tLndlYi5wYWdloW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdhKjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQP6o3NuZMQgvbASYXCX0pGddnnNoDyK5A6U3tG4JMsc+ZNdSRlcSzykdHlwZaRhY2Zn",
#         "Addresses": [
#             "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI",
#             "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
#             "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
#         ],
#         "Threshold": 2,
#         "SignerAddress": "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
#         "TypeName": "signandsubmit.mtx.algo",
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
#         mtx=gtuple.Mtx,
#         addresses=gtuple.Addresses,
#         threshold=gtuple.Threshold,
#         signer_address=gtuple.SignerAddress,
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
#     del d2["Mtx"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["Addresses"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["Threshold"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     d2 = dict(d)
#     del d2["SignerAddress"]
#     with pytest.raises(SchemaError):
#         Maker.dict_to_tuple(d2)

#     ######################################
#     # Behavior on incorrect types
#     ######################################

#     d2 = dict(d, Threshold="2.1")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)

#     ######################################
#     # SchemaError raised if TypeName is incorrect
#     ######################################

#     d2 = dict(d, TypeName="not the type alias")
#     with pytest.raises(ValidationError):
#         Maker.dict_to_tuple(d2)
