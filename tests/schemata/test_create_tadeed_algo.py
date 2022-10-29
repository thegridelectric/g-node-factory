"""Tests create.tadeed.algo.010 type"""
import json

import pytest
from errors import SchemaError
from schemata.create_tadeed_algo_maker import CreateTadeedAlgo_Maker as Maker


def test_create_tadeed_algo_generated():

    gw_dict = {
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "HalfSignedDeedCreationMtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCD8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBqFzxEA1Eb0A46T2R1Aym2+hIv+Bhf8b1POzeGd51noXYPYXd+7slYtEJ8W1qvOo3c0LzVIC5kPyU1Ud2Af0e5yKsMcHo3RocgKhdgGjdHhuiKRhcGFyhKJhbrRkdzEuaXNvLm1lLm9yYW5nZS50YaFtxCCLWHNvVZoPMX7bXlxHzGaJF9RAyueOoe1BXk+IUEBS2aF0AaJ1bqZUQURFRUSjZmVlzQPoomZ2zRgCo2dlbqpzYW5kbmV0LXYxomdoxCAv4hfmyOC1OlE4BuEiMcg9dD0tP7zQBGvdzguUlURZ+qJsds0b6qNzbmTEIMdnGF0JPZPHHFmVn8fmYiS7Wzi6UObcSZTp1gpcJYQHpHR5cGWkYWNmZw==",
        "TypeName": "create.tadeed.algo.010",
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
        validator_addr=gw_tuple.ValidatorAddr,
        half_signed_deed_creation_mtx=gw_tuple.HalfSignedDeedCreationMtx,
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

    orig_value = gw_dict["ValidatorAddr"]
    del gw_dict["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["HalfSignedDeedCreationMtx"]
    del gw_dict["HalfSignedDeedCreationMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedDeedCreationMtx"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = gw_dict["ValidatorAddr"]
    gw_dict["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["ValidatorAddr"] = orig_value

    orig_value = gw_dict["HalfSignedDeedCreationMtx"]
    gw_dict["HalfSignedDeedCreationMtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["HalfSignedDeedCreationMtx"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    gw_dict["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(gw_dict)
    gw_dict["TypeName"] = "create.tadeed.algo.010"
