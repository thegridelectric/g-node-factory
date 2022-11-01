"""Tests create.discoverycert.algo.001 type"""
import json

import pytest
from errors import SchemaError
from schemata.create_discoverycert_algo_maker import (
    CreateDiscoverycertAlgo_Maker as Maker,
)


def test_create_discoverycert_algo_generated():

    gw_dict = {
        "OldChildAliasList": ["d1.isone.ver.keene.holly"],
        "GNodeAlias": d1.isone.ver.keene,
        "DiscovererAddr": "KH3K4W3RXDUQNB2PUYSQECSK6RPP25NQUYYX6TYPTQBJAFG3K3O3B7KMZY",
        "MicroLon": -68705311,
        "SupportingMaterialHash": "hash of supporting material",
        "MicroLat": 44838681,
        "CoreGNodeRoleGtEnumSymbol": "4502e355",
        "TypeName": "create.discoverycert.algo.001",
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
        old_child_alias_list=gw_tuple.OldChildAliasList,
        g_node_alias=gw_tuple.GNodeAlias,
        core_g_node_role=gw_tuple.CoreGNodeRole,
        discoverer_addr=gw_tuple.DiscovererAddr,
        micro_lon=gw_tuple.MicroLon,
        supporting_material_hash=gw_tuple.SupportingMaterialHash,
        micro_lat=gw_tuple.MicroLat,
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

    orig_value = gw_dict["OldChildAliasList"]
    del gw_dict["OldChildAliasList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["OldChildAliasList"] = orig_value

    orig_value = gw_dict["GNodeAlias"]
    del gw_dict["GNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = orig_value

    orig_value = gw_dict["CoreGNodeRoleGtEnumSymbol"]
    del gw_dict["CoreGNodeRoleGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["CoreGNodeRoleGtEnumSymbol"] = orig_value

    orig_value = gw_dict["DiscovererAddr"]
    del gw_dict["DiscovererAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DiscovererAddr"] = orig_value

    orig_value = gw_dict["SupportingMaterialHash"]
    del gw_dict["SupportingMaterialHash"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["SupportingMaterialHash"] = orig_value

    ######################################
    # Optional attributes can be removed from type
    ######################################

    orig_value = gw_dict["MicroLon"]
    del gw_dict["MicroLon"]
    gw_type = json.dumps(gw_dict)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["MicroLat"]
    del gw_dict["MicroLat"]
    gw_type = json.dumps(gw_dict)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    gw_dict["MicroLat"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["OldChildAliasList"]
    gw_dict["OldChildAliasList"] = "This string is not a list."
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["OldChildAliasList"] = [42]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["OldChildAliasList"] = orig_value

    orig_value = gw_dict["GNodeAlias"]
    gw_dict["GNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = orig_value

    with pytest.raises(SchemaError):
        Maker(
            old_child_alias_list=gw_tuple.OldChildAliasList,
            g_node_alias=gw_tuple.GNodeAlias,
            discoverer_addr=gw_tuple.DiscovererAddr,
            micro_lon=gw_tuple.MicroLon,
            supporting_material_hash=gw_tuple.SupportingMaterialHash,
            micro_lat=gw_tuple.MicroLat,
            core_g_node_role="This is not a CoreGNodeRole Enum.",
        )

    orig_value = gw_dict["DiscovererAddr"]
    gw_dict["DiscovererAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DiscovererAddr"] = orig_value

    orig_value = gw_dict["MicroLon"]
    gw_dict["MicroLon"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLon"] = orig_value

    orig_value = gw_dict["SupportingMaterialHash"]
    gw_dict["SupportingMaterialHash"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["SupportingMaterialHash"] = orig_value

    orig_value = gw_dict["MicroLat"]
    gw_dict["MicroLat"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["MicroLat"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "create.discoverycert.algo.001"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    gw_dict["OldChildAliasList"] = ["a.b-h"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["OldChildAliasList"] = ["d1.isone.ver.keene.holly"]

    gw_dict["GNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = d1.isone.ver.keene

    # End of Test
