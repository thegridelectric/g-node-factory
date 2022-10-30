"""Tests status.basegnode.010 type"""
import json

import pytest
from errors import SchemaError
from schemata.status_basegnode_maker import StatusBasegnode_Maker as Maker


def test_status_basegnode_generated():

    gw_dict = {
        "IncludeAllDescendants": True,
        "DescendantGNodeList": "FixMe",
        "FromGNodeAlias": "dwgps.gnr",
        "FromGNodeInstanceId": "f5de29a7-1e72-4627-818e-dc527a889fda",
        "ToGNodeAlias": "dwgps.gnf",
        "TopGNodeId": "FixMe",
        "TypeName": "status.basegnode.010",
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
        include_all_descendants=gw_tuple.IncludeAllDescendants,
        descendant_g_node_list_id=gw_tuple.DescendantGNodeListId,
        from_g_node_alias=gw_tuple.FromGNodeAlias,
        from_g_node_instance_id=gw_tuple.FromGNodeInstanceId,
        top_g_node_id=gw_tuple.TopGNodeId,
        to_g_node_alias=gw_tuple.ToGNodeAlias,
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

    orig_value = gw_dict["IncludeAllDescendants"]
    del gw_dict["IncludeAllDescendants"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["IncludeAllDescendants"] = orig_value

    orig_value = gw_dict["DescendantGNodeList"]
    del gw_dict["DescendantGNodeList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DescendantGNodeList"] = orig_value

    orig_value = gw_dict["FromGNodeAlias"]
    del gw_dict["FromGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    orig_value = gw_dict["FromGNodeInstanceId"]
    del gw_dict["FromGNodeInstanceId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = orig_value

    orig_value = gw_dict["TopGNodeId"]
    del gw_dict["TopGNodeId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TopGNodeId"] = orig_value

    orig_value = gw_dict["ToGNodeAlias"]
    del gw_dict["ToGNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ToGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["IncludeAllDescendants"]
    gw_dict["IncludeAllDescendants"] = "This string is not a boolean."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["IncludeAllDescendants"] = orig_value

    orig_value = gw_dict["DescendantGNodeListId"]
    gw_dict["DescendantGNodeListId"] = "Not a dataclass id"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DescendantGNodeListId"] = orig_value

    orig_value = gw_dict["DescendantGNodeList"]
    gw_dict["DescendantGNodeList"] = "Not a list."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DescendantGNodeList"] = orig_value

    orig_value = gw_dict["DescendantGNodeList"]
    gw_dict["DescendantGNodeList"] = ["Not even a dict"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)

    gw_dict["DescendantGNodeList"] = [{"Failed": "Not a GtSimpleSingleStatus"}]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DescendantGNodeList"] = orig_value

    with pytest.raises(SchemaError):
        Maker(
            include_all_descendants=gw_dict["IncludeAllDescendants"],
            from_g_node_alias=gw_dict["FromGNodeAlias"],
            from_g_node_instance_id=gw_dict["FromGNodeInstanceId"],
            top_g_node=gw_dict["TopGNode"],
            to_g_node_alias=gw_dict["ToGNodeAlias"],
            descendant_g_node_list=["Not a Basegnode010"],
        )

    with pytest.raises(SchemaError):
        Maker(
            include_all_descendants=gw_tuple.IncludeAllDescendants,
            from_g_node_alias=gw_tuple.FromGNodeAlias,
            from_g_node_instance_id=gw_tuple.FromGNodeInstanceId,
            top_g_node=gw_tuple.TopGNode,
            to_g_node_alias=gw_tuple.ToGNodeAlias,
            descendant_g_node_list="This string is not a list",
        )

    orig_value = gw_dict["FromGNodeAlias"]
    gw_dict["FromGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = orig_value

    orig_value = gw_dict["FromGNodeInstanceId"]
    gw_dict["FromGNodeInstanceId"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = orig_value

    orig_value = gw_dict["TopGNodeId"]
    gw_dict["TopGNodeId"] = "Not a dataclass id"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TopGNodeId"] = orig_value

    orig_value = gw_dict["ToGNodeAlias"]
    gw_dict["ToGNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ToGNodeAlias"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "status.basegnode.010"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    gw_dict["FromGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeAlias"] = "dwgps.gnr"

    gw_dict["FromGNodeInstanceId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["FromGNodeInstanceId"] = "f5de29a7-1e72-4627-818e-dc527a889fda"

    gw_dict["ToGNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ToGNodeAlias"] = "dwgps.gnf"

    # End of Test
