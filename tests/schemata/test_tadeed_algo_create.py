"""Tests tadeed.algo.create type, version 000"""
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import TadeedAlgoCreate_Maker as Maker


def test_tadeed_algo_create_generated():

    d = {
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "HalfSignedDeedCreationMtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCD8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBqFzxEA1Eb0A46T2R1Aym2+hIv+Bhf8b1POzeGd51noXYPYXd+7slYtEJ8W1qvOo3c0LzVIC5kPyU1Ud2Af0e5yKsMcHo3RocgKhdgGjdHhuiKRhcGFyhKJhbrRkdzEuaXNvLm1lLm9yYW5nZS50YaFtxCCLWHNvVZoPMX7bXlxHzGaJF9RAyueOoe1BXk+IUEBS2aF0AaJ1bqZUQURFRUSjZmVlzQPoomZ2zRgCo2dlbqpzYW5kbmV0LXYxomdoxCAv4hfmyOC1OlE4BuEiMcg9dD0tP7zQBGvdzguUlURZ+qJsds0b6qNzbmTEIMdnGF0JPZPHHFmVn8fmYiS7Wzi6UObcSZTp1gpcJYQHpHR5cGWkYWNmZw==",
        "TypeName": "tadeed.algo.create",
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
        validator_addr=gtuple.ValidatorAddr,
        half_signed_deed_creation_mtx=gtuple.HalfSignedDeedCreationMtx,
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
    del d2["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["HalfSignedDeedCreationMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Behavior on incorrect types
    ######################################

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d2 = dict(d, TypeName="not the type alias")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)
