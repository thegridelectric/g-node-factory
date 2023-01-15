"""Tests basegnodes.broadcast type, version 000"""
import json

import pytest
from gridworks.errors import SchemaError
from pydantic import ValidationError

from gnf.types import BasegnodesBroadcast_Maker as Maker


def test_basegnodes_broadcast_generated() -> None:
    d = {
        "FromGNodeAlias": "dwgps.gnf",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "IncludeAllDescendants": True,
        "TopGNode": {
            "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
            "Alias": "d1",
            "StatusGtEnumSymbol": "153d3475",
            "RoleGtEnumSymbol": "00000000",
            "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
            "TypeName": "basegnode.gt",
            "Version": "020",
        },
        "DescendantGNodeList": [
            {
                "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
                "Alias": "d1",
                "StatusGtEnumSymbol": "153d3475",
                "RoleGtEnumSymbol": "00000000",
                "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
                "TypeName": "basegnode.gt",
                "Version": "020",
            },
            {
                "GNodeId": "c0119953-a48f-495d-87cc-58fb92eb4cee",
                "Alias": "d1.isone",
                "StatusGtEnumSymbol": "153d3475",
                "RoleGtEnumSymbol": "4502e355",
                "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
                "TypeName": "basegnode.gt",
                "Version": "020",
            },
        ],
        "TypeName": "basegnodes.broadcast",
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
        from_g_node_alias=gtuple.FromGNodeAlias,
        from_g_node_instance_id=gtuple.FromGNodeInstanceId,
        include_all_descendants=gtuple.IncludeAllDescendants,
        top_g_node=gtuple.TopGNode,
        descendant_g_node_list=gtuple.DescendantGNodeList,
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
    del d2["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["IncludeAllDescendants"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["TopGNode"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["DescendantGNodeList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, IncludeAllDescendants="this is not a boolean")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, DescendantGNodeList="Not a list.")
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, DescendantGNodeList=["Not a list of dicts"])
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, DescendantGNodeList=[{"Failed": "Not a GtSimpleSingleStatus"}])
    with pytest.raises(SchemaError):
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

    d2 = dict(d, FromGNodeAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, FromGNodeInstanceId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
