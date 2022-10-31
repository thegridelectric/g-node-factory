"""Tests create.validatorcert.algo.010 type"""
import json

import pytest

from gnf.errors import SchemaError
from gnf.schemata import CreateTavalidatorcertAlgo_Maker as Maker


def test_create_validatorcert_algo():

    gw_dict = {
        "HalfSignedCertCreationMtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCCaszbRc+Y8G+clVkPcnrpfOvDkLUKVB3r+nOM5G4mCaqFzxEAYjou1knNqJfnQ/Hf+9BR5Q3iODO9lLK/k3raQokAGxcmoNYXJvONGUllxbsX2LgdkdA+Zl1C7s8MRKTK1DHQKo3RocgKhdgGjdHhuiKRhcGFyhaJhbq5UZXN0IFZhbGlkYXRvcqJhdbZodHRwOi8vcmFuZG9tLndlYi5wYWdloW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdhKjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQP6o3NuZMQgvbASYXCX0pGddnnNoDyK5A6U3tG4JMsc+ZNdSRlcSzykdHlwZaRhY2Zn",
        "ValidatorAddr": "TKZTNULT4Y6BXZZFKZB5ZHV2L45PBZBNIKKQO6X6TTRTSG4JQJVB7VKMHU",
        "TypeName": "create.tavalidatorcert.algo.010",
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
        half_signed_cert_creation_mtx=gw_tuple.HalfSignedCertCreationMtx,
        validator_addr=gw_tuple.ValidatorAddr,
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

    orig_value = gw_dict["HalfSignedCertCreationMtx"]
    del gw_dict["HalfSignedCertCreationMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedCertCreationMtx"] = orig_value

    orig_value = gw_dict["ValidatorAddr"]
    del gw_dict["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["HalfSignedCertCreationMtx"]
    gw_dict["HalfSignedCertCreationMtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedCertCreationMtx"] = orig_value

    orig_value = gw_dict["ValidatorAddr"]
    gw_dict["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "create.validatorcert.algo.010"
