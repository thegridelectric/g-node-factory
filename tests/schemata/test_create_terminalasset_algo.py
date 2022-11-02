"""Tests create.terminalasset.algo type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import CreateTerminalassetAlgo
from gnf.schemata import CreateTerminalassetAlgo_Maker as Maker


def test_create_terminalasset_algo_generated():

    d = {
        "TaGNodeAlias": "dw1.iso.me.orange.ta",
        "MicroLon": -68691705,
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
        "MicroLat": 45666353,
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "FromGNodeAlias": "dwgps.gnr",
        "TypeName": "create.terminalasset.algo",
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

    orig_value = d["TypeName"]
    del d["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = orig_value

    orig_value = d["TaGNodeAlias"]
    del d["TaGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TaGNodeAlias"] = orig_value

    orig_value = d["MicroLon"]
    del d["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLon"] = orig_value

    orig_value = d["ValidatorAddr"]
    del d["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ValidatorAddr"] = orig_value

    orig_value = d["TaOwnerAddr"]
    del d["TaOwnerAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TaOwnerAddr"] = orig_value

    orig_value = d["MicroLat"]
    del d["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLat"] = orig_value

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

    orig_value = d["FromGNodeAlias"]
    del d["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = d["TaGNodeAlias"]
    d["TaGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TaGNodeAlias"] = orig_value

    orig_value = d["MicroLon"]
    d["MicroLon"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLon"] = orig_value

    orig_value = d["ValidatorAddr"]
    d["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ValidatorAddr"] = orig_value

    orig_value = d["TaOwnerAddr"]
    d["TaOwnerAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TaOwnerAddr"] = orig_value

    orig_value = d["MicroLat"]
    d["MicroLat"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["MicroLat"] = orig_value

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

    orig_value = d["FromGNodeAlias"]
    d["FromGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "create.terminalasset.algo"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d["TaGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TaGNodeAlias"] = "dw1.iso.me.orange.ta"

    d["FromGNodeInstanceId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeInstanceId"] = "f5de29a7-1e72-4627-818e-dc527a889fda"

    d["FromGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["FromGNodeAlias"] = "dwgps.gnr"

    # End of Test
