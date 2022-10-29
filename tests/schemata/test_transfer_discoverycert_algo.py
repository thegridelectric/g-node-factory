"""Tests transfer.discoverycert.algo.001 type"""
import json

import pytest
from errors import SchemaError
from schemata.transfer_discoverycert_algo_maker import (
    TransferDiscoverycertAlgo_Maker as Maker,
)


def test_transfer_discoverycert_algo_generated():

    gw_dict = {
        "GNodeAlias": "d1.isone.ver.keene.pwrs",
        "DiscovererAddr": "KH3K4W3RXDUQNB2PUYSQECSK6RPP25NQUYYX6TYPTQBJAFG3K3O3B7KMZY",
        "TypeName": "transfer.discoverycert.algo.001",
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
        g_node_alias=gw_tuple.GNodeAlias,
        discoverer_addr=gw_tuple.DiscovererAddr,
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

    orig_value = gw_dict["GNodeAlias"]
    del gw_dict["GNodeAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = orig_value

    orig_value = gw_dict["DiscovererAddr"]
    del gw_dict["DiscovererAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DiscovererAddr"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["GNodeAlias"]
    gw_dict["GNodeAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = orig_value

    orig_value = gw_dict["DiscovererAddr"]
    gw_dict["DiscovererAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["DiscovererAddr"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "transfer.discoverycert.algo.001"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    gw_dict["GNodeAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["GNodeAlias"] = "d1.isone.ver.keene.pwrs"

    # End of Test
