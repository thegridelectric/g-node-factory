"""Tests discoverycert.algo.create type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gnf.enums import CoreGNodeRole
from gnf.errors import SchemaError
from gnf.schemata import DiscoverycertAlgoCreate_Maker as Maker


def test_discoverycert_algo_create_generated():

    d = {
        "GNodeAlias": "d1.isone.ver.keene",
        "CoreGNodeRoleGtEnumSymbol": "4502e355",
        "OldChildAliasList": ["dw1.isone.ver.keene.holly"],
        "DiscovererAddr": "KH3K4W3RXDUQNB2PUYSQECSK6RPP25NQUYYX6TYPTQBJAFG3K3O3B7KMZY",
        "SupportingMaterialHash": "hash of supporting material",
        "MicroLat": 44838681,
        "MicroLon": -68705311,
        "TypeName": "discoverycert.algo.create",
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
        g_node_alias=gtuple.GNodeAlias,
        core_g_node_role=gtuple.CoreGNodeRole,
        old_child_alias_list=gtuple.OldChildAliasList,
        discoverer_addr=gtuple.DiscovererAddr,
        supporting_material_hash=gtuple.SupportingMaterialHash,
        micro_lat=gtuple.MicroLat,
        micro_lon=gtuple.MicroLon,
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
    del d2["GNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["CoreGNodeRoleGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["OldChildAliasList"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["DiscovererAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["SupportingMaterialHash"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Optional attributes can be removed from type
    ######################################

    d2 = dict(d)
    if "MicroLat" in d2.keys():
        del d2["MicroLat"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "MicroLon" in d2.keys():
        del d2["MicroLon"]
    Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, CoreGNodeRoleGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).CoreGNodeRole = CoreGNodeRole.default()

    d2 = dict(d, MicroLat="44838681.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, MicroLon="-68705311.1")
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

    d2 = dict(d, GNodeAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, OldChildAliasList=["a.b-h"])
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
