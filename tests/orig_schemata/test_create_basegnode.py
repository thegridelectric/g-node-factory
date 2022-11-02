"""Tests create.basegnode.010 type"""
import json

import pytest

from gnf.errors import SchemaError
from gnf.schemata import CreateBasegnode_Maker as Maker


def test_create_basegnode_generated():

    d = {
        "GNodeId": "9405686a-14fd-4aef-945b-cd7c97903f14",
        "Alias": "dw1.iso.me.orange.ta",
        "StatusGtEnumSymbol": "3661506b",
        "RoleGtEnumSymbol": "0f8872f7",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "GpsPointId": "50f3f6e8-5937-47c2-8d05-06525ef6467d",
        "OwnershipDeedNftId": 5,
        "OwnershipDeedValidatorAddr": "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI",
        "TypeName": "basegnode.gt",
        "Version": "020",
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

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "create.basegnode.010"
