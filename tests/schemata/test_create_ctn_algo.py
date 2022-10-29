"""Tests create.ctn.algo.001 type"""
import json

import pytest
from errors import SchemaError
from schemata.create_ctn_algo_maker import CreateCtnAlgo_Maker as Maker


def test_create_ctn_algo_generated():

    gw_dict = {
        "ChildAliasList": ["d1.isone.ver.keene.holly", "d1.isone.ver.keene.orange"],
        "FromGNodeAlias": "dwgps.gnr",
        "MicroLat": 44838681,
        "MicroLon": -68705311,
        "CtnGNodeAlias": "d1.isone.ver.keene.pwrs",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "TypeName": "create.ctn.algo.001",
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
        child_alias_list=gw_tuple.ChildAliasList,
        from_g_node_alias=gw_tuple.FromGNodeAlias,
        micro_lat=gw_tuple.MicroLat,
        micro_lon=gw_tuple.MicroLon,
        ctn_g_node_alias=gw_tuple.CtnGNodeAlias,
        g_node_registry_addr=gw_tuple.GNodeRegistryAddr,
        from_g_node_instance_id=gw_tuple.FromGNodeInstanceId,
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

    orig_value = gw_dict["ChildAliasList"]
    del gw_dict["ChildAliasList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ChildAliasList"] = orig_value

    orig_value = gw_dict["FromGNodeAlias"]
    del gw_dict["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    orig_value = gw_dict["MicroLat"]
    del gw_dict["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLat"] = orig_value

    orig_value = gw_dict["MicroLon"]
    del gw_dict["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["CtnGNodeAlias"]
    del gw_dict["CtnGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["CtnGNodeAlias"] = orig_value

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

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["ChildAliasList"]
    gw_dict["ChildAliasList"] = "This string is not a list."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ChildAliasList"] = [42]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ChildAliasList"] = orig_value

    orig_value = gw_dict["FromGNodeAlias"]
    gw_dict["FromGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    orig_value = gw_dict["MicroLat"]
    gw_dict["MicroLat"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLat"] = orig_value

    orig_value = gw_dict["MicroLon"]
    gw_dict["MicroLon"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["CtnGNodeAlias"]
    gw_dict["CtnGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["CtnGNodeAlias"] = orig_value

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

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "create.ctn.algo.001"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    gw_dict["ChildAliasList"] = ["a.b-h"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ChildAliasList"] = ["dw1.iso.me.orange", "dw1.iso.me.almond"]

    gw_dict["FromGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = "dwgps.gnr"

    gw_dict["CtnGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["CtnGNodeAlias"] = "dw1.iso.me.ghm.orange.ta"

    gw_dict["FromGNodeInstanceId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = "f5de29a7-1e72-4627-818e-dc527a889fda"

    # End of Test
