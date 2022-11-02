"""Tests create.ctn.algo type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import CreateCtnAlgo
from gnf.schemata import CreateCtnAlgo_Maker as Maker


def test_create_ctn_algo_generated():

    d = {
        "ChildAliasList": ["dw1.iso.me.orange", "dw1.iso.me.almond"],
        "FromGNodeAlias": "dwgps.gnr",
        "MicroLat": 44838681,
        "MicroLon": -68705311,
        "CtnGNodeAlias": "dw1.iso.me.ghm.orange.ta",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "TypeName": "create.ctn.algo",
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

    orig_value = d["TypeName"]
    del d["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = orig_value

    orig_value = d["ChildAliasList"]
    del d["ChildAliasList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ChildAliasList"] = orig_value

    orig_value = d["FromGNodeAlias"]
    del d["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = orig_value

    orig_value = d["MicroLat"]
    del d["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLat"] = orig_value

    orig_value = d["MicroLon"]
    del d["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLon"] = orig_value

    orig_value = d["CtnGNodeAlias"]
    del d["CtnGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["CtnGNodeAlias"] = orig_value

    orig_value = d["GNodeRegistryAddr"]
    del d["GNodeRegistryAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeRegistryAddr"] = orig_value

    orig_value = d["FromGNodeInstanceId"]
    del d["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeInstanceId"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = d["ChildAliasList"]
    d["ChildAliasList"] = "This string is not a list."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ChildAliasList"] = [42]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ChildAliasList"] = orig_value

    orig_value = d["FromGNodeAlias"]
    d["FromGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = orig_value

    orig_value = d["MicroLat"]
    d["MicroLat"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLat"] = orig_value

    orig_value = d["MicroLon"]
    d["MicroLon"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLon"] = orig_value

    orig_value = d["CtnGNodeAlias"]
    d["CtnGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["CtnGNodeAlias"] = orig_value

    orig_value = d["GNodeRegistryAddr"]
    d["GNodeRegistryAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeRegistryAddr"] = orig_value

    orig_value = d["FromGNodeInstanceId"]
    d["FromGNodeInstanceId"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeInstanceId"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "create.ctn.algo"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d["ChildAliasList"] = ["a.b-h"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ChildAliasList"] = ["dw1.iso.me.orange", "dw1.iso.me.almond"]

    d["FromGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = "dwgps.gnr"

    d["CtnGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["CtnGNodeAlias"] = "dw1.iso.me.ghm.orange.ta"

    d["FromGNodeInstanceId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeInstanceId"] = "f5de29a7-1e72-4627-818e-dc527a889fda"

    # End of Test
