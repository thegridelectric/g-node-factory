"""Tests signandsubmit.mtx.algo type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import SignandsubmitMtxAlgo
from gnf.schemata import SignandsubmitMtxAlgo_Maker as Maker


def test_signandsubmit_mtx_algo_generated():

    d = {
        "SignerAddress": "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
        "Mtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCCaszbRc+Y8G+clVkPcnrpfOvDkLUKVB3r+nOM5G4mCaqFzxEAYjou1knNqJfnQ/Hf+9BR5Q3iODO9lLK/k3raQokAGxcmoNYXJvONGUllxbsX2LgdkdA+Zl1C7s8MRKTK1DHQKo3RocgKhdgGjdHhuiKRhcGFyhaJhbq5UZXN0IFZhbGlkYXRvcqJhdbZodHRwOi8vcmFuZG9tLndlYi5wYWdloW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdhKjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQP6o3NuZMQgvbASYXCX0pGddnnNoDyK5A6U3tG4JMsc+ZNdSRlcSzykdHlwZaRhY2Zn",
        "Addresses": [
            "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI",
            "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
            "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
        ],
        "Threshold": 2,
        "TypeName": "signandsubmit.mtx.algo",
        "Version": "",
    }

    with pytest.raises(SchemaError):
        Maker.type_to_tuple(d)

    with pytest.raises(SchemaError):
        Maker.type_to_tuple('"not a dict"')

    # Test type_to_tuple
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)

    # test type_to_tuple and tuple_to_type maps
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple

    # test Maker init
    t = Maker(
        signer_address=gw_tuple.SignerAddress,
        mtx=gw_tuple.Mtx,
        addresses=gw_tuple.Addresses,
        threshold=gw_tuple.Threshold,
        #
    ).tuple
    assert t == gw_tuple

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    orig_value = d["TypeName"]
    del d["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = orig_value

    orig_value = d["SignerAddress"]
    del d["SignerAddress"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["SignerAddress"] = orig_value

    orig_value = d["Mtx"]
    del d["Mtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Mtx"] = orig_value

    orig_value = d["Addresses"]
    del d["Addresses"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Addresses"] = orig_value

    orig_value = d["Threshold"]
    del d["Threshold"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Threshold"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = d["SignerAddress"]
    d["SignerAddress"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["SignerAddress"] = orig_value

    orig_value = d["Mtx"]
    d["Mtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Mtx"] = orig_value

    orig_value = d["Addresses"]
    d["Addresses"] = "This string is not a list."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Addresses"] = [42]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Addresses"] = orig_value

    orig_value = d["Threshold"]
    d["Threshold"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Threshold"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "signandsubmit.mtx.algo"
