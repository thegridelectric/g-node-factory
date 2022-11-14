"""Tests tadeed.specs.private.hack type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import TadeedSpecsPrivateHack_Maker as Maker


def test_tadeed_specs_private_hack_generated() -> None:

    d = {
        "TerminalAssetAlias": "d1.isone.ver.keene.holly.ta",
        "TaOwnerSk": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
        "TaDaemonSk": "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
        "MicroLat": 45666353,
        "MicroLon": 68691705,
        "TypeName": "tadeed.specs.private.hack",
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
        terminal_asset_alias=gtuple.TerminalAssetAlias,
        ta_owner_sk=gtuple.TaOwnerSk,
        ta_daemon_sk=gtuple.TaDaemonSk,
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
    del d2["TerminalAssetAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["TaOwnerSk"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["TaDaemonSk"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["MicroLat"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["MicroLon"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    d2 = dict(d, MicroLat="45666353.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, MicroLon="68691705.1")
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

    d2 = dict(d, TerminalAssetAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
