"""Tests heartbeat.a.100 type"""
import json

import pytest
from errors import SchemaError
from schemata.heartbeat_a_maker import HeartbeatA_Maker as Maker


def test_heartbeat_a_generated():

    gw_dict = {
        "TypeName": "heartbeat.a.100",
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

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "heartbeat.a.100"
