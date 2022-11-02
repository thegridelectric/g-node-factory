"""Tests create.terminalasset.algo.010 type"""
import json

import pytest

from gnf.errors import SchemaError
from gnf.schemata import CreateTerminalassetAlgo_Maker as Maker


def test_create_terminalasset_algo_generated():

    gw_dict = {
        "TaGNodeAlias": "d1.isone.ver.keene.holly.ta",
        "MicroLon": -68691705,
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
        "MicroLat": 45666353,
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "FromGNodeAlias": "dwgps.gnr",
        "TypeName": "create.terminalasset.algo.010",
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
        ta_g_node_alias=gw_tuple.TaGNodeAlias,
        micro_lon=gw_tuple.MicroLon,
        validator_addr=gw_tuple.ValidatorAddr,
        ta_owner_addr=gw_tuple.TaOwnerAddr,
        micro_lat=gw_tuple.MicroLat,
        g_node_registry_addr=gw_tuple.GNodeRegistryAddr,
        from_g_node_instance_id=gw_tuple.FromGNodeInstanceId,
        from_g_node_alias=gw_tuple.FromGNodeAlias,
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

    orig_value = gw_dict["TaGNodeAlias"]
    del gw_dict["TaGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaGNodeAlias"] = orig_value

    orig_value = gw_dict["MicroLon"]
    del gw_dict["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["ValidatorAddr"]
    del gw_dict["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["TaOwnerAddr"]
    del gw_dict["TaOwnerAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaOwnerAddr"] = orig_value

    orig_value = gw_dict["MicroLat"]
    del gw_dict["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLat"] = orig_value

    orig_value = gw_dict["GNodeRegistryAddr"]
    del gw_dict["GNodeRegistryAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeRegistryAddr"] = orig_value

    orig_value = gw_dict["FromGNodeInstanceId"]
    del gw_dict["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = orig_value

    orig_value = gw_dict["FromGNodeAlias"]
    del gw_dict["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["TaGNodeAlias"]
    gw_dict["TaGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaGNodeAlias"] = orig_value

    orig_value = gw_dict["MicroLon"]
    gw_dict["MicroLon"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["ValidatorAddr"]
    gw_dict["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["TaOwnerAddr"]
    gw_dict["TaOwnerAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaOwnerAddr"] = orig_value

    orig_value = gw_dict["MicroLat"]
    gw_dict["MicroLat"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLat"] = orig_value

    orig_value = gw_dict["GNodeRegistryAddr"]
    gw_dict["GNodeRegistryAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeRegistryAddr"] = orig_value

    orig_value = gw_dict["FromGNodeInstanceId"]
    gw_dict["FromGNodeInstanceId"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = orig_value

    orig_value = gw_dict["FromGNodeAlias"]
    gw_dict["FromGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "create.terminalasset.algo.010"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    gw_dict["TaGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TaGNodeAlias"] = "dw1.iso.me.orange.ta"

    gw_dict["FromGNodeInstanceId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = "f5de29a7-1e72-4627-818e-dc527a889fda"

    gw_dict["FromGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = "dwgps.gnr"

    # End of Test
