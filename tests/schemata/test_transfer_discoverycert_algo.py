"""Tests transfer.discoverycert.algo type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import TransferDiscoverycertAlgo
from gnf.schemata import TransferDiscoverycertAlgo_Maker as Maker


def test_transfer_discoverycert_algo_generated():

    d = {
        "GNodeAlias": "d1.isone.ver.keene.pwrs",
        "DiscovererAddr": "KH3K4W3RXDUQNB2PUYSQECSK6RPP25NQUYYX6TYPTQBJAFG3K3O3B7KMZY",
        "TypeName": "transfer.discoverycert.algo",
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
        g_node_alias=gw_tuple.GNodeAlias,
        discoverer_addr=gw_tuple.DiscovererAddr,
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

    orig_value = d["GNodeAlias"]
    del d["GNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeAlias"] = orig_value

    orig_value = d["DiscovererAddr"]
    del d["DiscovererAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["DiscovererAddr"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = d["GNodeAlias"]
    d["GNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeAlias"] = orig_value

    orig_value = d["DiscovererAddr"]
    d["DiscovererAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["DiscovererAddr"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "transfer.discoverycert.algo"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d["GNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeAlias"] = "d1.isone.ver.keene.pwrs"

    # End of Test
