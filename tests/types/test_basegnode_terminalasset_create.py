"""Tests basegnode.terminalasset.create type, version 000"""
import json

import pytest
from gridworks.errors import SchemaError
from pydantic import ValidationError

from gnf.types import BasegnodeTerminalassetCreate_Maker as Maker


def test_basegnode_terminalasset_create_generated() -> None:
    d = {
        "TaGNodeAlias": "d1.iso.me.orange.ta",
        "MicroLon": -68691705,
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
        "MicroLat": 45666353,
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "FromGNodeAlias": "dwgps.gnr",
        "TypeName": "basegnode.terminalasset.create",
        "Version": "000",
    }

    with pytest.raises(SchemaError):
        Maker.type_to_tuple(d)

    with pytest.raises(SchemaError):
        Maker.type_to_tuple('"not a dict"')

    # Test type_to_tuple
    gtype = json.dumps(d)
    gtuple = Maker.type_to_tuple(gtype)

    # test type_to_tuple and tuple_to_type maps
    assert Maker.type_to_tuple(Maker.tuple_to_type(gtuple)) == gtuple

    # test Maker init
    t = Maker(
        ta_g_node_alias=gtuple.TaGNodeAlias,
        micro_lon=gtuple.MicroLon,
        validator_addr=gtuple.ValidatorAddr,
        ta_owner_addr=gtuple.TaOwnerAddr,
        micro_lat=gtuple.MicroLat,
        g_node_registry_addr=gtuple.GNodeRegistryAddr,
        from_g_node_instance_id=gtuple.FromGNodeInstanceId,
        from_g_node_alias=gtuple.FromGNodeAlias,
    ).tuple
    assert t == gtuple

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    d2 = dict(d)
    del d2["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["TaGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["TaOwnerAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["GNodeRegistryAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, MicroLon="-68691705.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, MicroLat="45666353.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d2 = dict(d, TaGNodeAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, FromGNodeInstanceId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, FromGNodeAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
