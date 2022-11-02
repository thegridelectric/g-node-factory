"""Tests basegnode.gt type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker as Maker


def test_basegnode_gt_generated():

    d = {
        "GNodeId": "9405686a-14fd-4aef-945b-cd7c97903f14",
        "Alias": "dw1.iso.me.orange.ta",
        "StatusGtEnumSymbol": "3661506b",
        "RoleGtEnumSymbol": "0f8872f7",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "GpsPointId": "50f3f6e8-5937-47c2-8d05-06525ef6467d",
        "OwnershipDeedNftId": 5,
        "OwnershipDeedValidatorAddr": "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI",
        "PrevAlias": "dw1",
        "OwnerAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "DaemonAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "TradingRightsNftId": 1,
        "TypeName": "basegnode.gt",
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
        status=gw_tuple.Status,
        g_node_registry_addr=gw_tuple.GNodeRegistryAddr,
        role=gw_tuple.Role,
        prev_alias=gw_tuple.PrevAlias,
        trading_rights_nft_id=gw_tuple.TradingRightsNftId,
        ownership_deed_validator_addr=gw_tuple.OwnershipDeedValidatorAddr,
        alias=gw_tuple.Alias,
        g_node_id=gw_tuple.GNodeId,
        ownership_deed_nft_id=gw_tuple.OwnershipDeedNftId,
        owner_addr=gw_tuple.OwnerAddr,
        daemon_addr=gw_tuple.DaemonAddr,
        gps_point_id=gw_tuple.GpsPointId,
        #
    ).tuple
    assert t == gw_tuple

    ######################################
    # Dataclass related tests
    ######################################

    dc = Maker.tuple_to_dc(gw_tuple)
    assert gw_tuple == Maker.dc_to_tuple(dc)
    assert Maker.type_to_dc(Maker.dc_to_type(dc)) == dc

    ######################################
    # SchemaError raised if missing a required attribute
    ######################################

    orig_value = d["TypeName"]
    del d["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = orig_value

    orig_value = d["StatusGtEnumSymbol"]
    del d["StatusGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["StatusGtEnumSymbol"] = orig_value

    orig_value = d["GNodeRegistryAddr"]
    del d["GNodeRegistryAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeRegistryAddr"] = orig_value

    orig_value = d["RoleGtEnumSymbol"]
    del d["RoleGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["RoleGtEnumSymbol"] = orig_value

    orig_value = d["Alias"]
    del d["Alias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Alias"] = orig_value

    orig_value = d["GNodeId"]
    del d["GNodeId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeId"] = orig_value

    ######################################
    # Optional attributes can be removed from type
    ######################################

    orig_value = d["PrevAlias"]
    del d["PrevAlias"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["PrevAlias"] = orig_value

    orig_value = d["TradingRightsNftId"]
    del d["TradingRightsNftId"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["TradingRightsNftId"] = orig_value

    orig_value = d["OwnershipDeedValidatorAddr"]
    del d["OwnershipDeedValidatorAddr"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["OwnershipDeedValidatorAddr"] = orig_value

    orig_value = d["OwnershipDeedNftId"]
    del d["OwnershipDeedNftId"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["OwnershipDeedNftId"] = orig_value

    orig_value = d["OwnerAddr"]
    del d["OwnerAddr"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["OwnerAddr"] = orig_value

    orig_value = d["DaemonAddr"]
    del d["DaemonAddr"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["DaemonAddr"] = orig_value

    orig_value = d["GpsPointId"]
    del d["GpsPointId"]
    gw_type = json.dumps(d)
    gw_tuple = Maker.type_to_tuple(gw_type)
    assert Maker.type_to_tuple(Maker.tuple_to_type(gw_tuple)) == gw_tuple
    d["GpsPointId"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    with pytest.raises(SchemaError):
        Maker(
            g_node_registry_addr=gw_tuple.GNodeRegistryAddr,
            role=gw_tuple.Role,
            prev_alias=gw_tuple.PrevAlias,
            trading_rights_nft_id=gw_tuple.TradingRightsNftId,
            ownership_deed_validator_addr=gw_tuple.OwnershipDeedValidatorAddr,
            alias=gw_tuple.Alias,
            g_node_id=gw_tuple.GNodeId,
            ownership_deed_nft_id=gw_tuple.OwnershipDeedNftId,
            owner_addr=gw_tuple.OwnerAddr,
            daemon_addr=gw_tuple.DaemonAddr,
            gps_point_id=gw_tuple.GpsPointId,
            status="This is not a GNodeStatus Enum.",
        )

    orig_value = d["GNodeRegistryAddr"]
    d["GNodeRegistryAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeRegistryAddr"] = orig_value

    with pytest.raises(SchemaError):
        Maker(
            status=gw_tuple.Status,
            g_node_registry_addr=gw_tuple.GNodeRegistryAddr,
            prev_alias=gw_tuple.PrevAlias,
            trading_rights_nft_id=gw_tuple.TradingRightsNftId,
            ownership_deed_validator_addr=gw_tuple.OwnershipDeedValidatorAddr,
            alias=gw_tuple.Alias,
            g_node_id=gw_tuple.GNodeId,
            ownership_deed_nft_id=gw_tuple.OwnershipDeedNftId,
            owner_addr=gw_tuple.OwnerAddr,
            daemon_addr=gw_tuple.DaemonAddr,
            gps_point_id=gw_tuple.GpsPointId,
            role="This is not a CoreGNodeRole Enum.",
        )

    orig_value = d["PrevAlias"]
    d["PrevAlias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["PrevAlias"] = orig_value

    orig_value = d["TradingRightsNftId"]
    d["TradingRightsNftId"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TradingRightsNftId"] = orig_value

    orig_value = d["OwnershipDeedValidatorAddr"]
    d["OwnershipDeedValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["OwnershipDeedValidatorAddr"] = orig_value

    orig_value = d["Alias"]
    d["Alias"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Alias"] = orig_value

    orig_value = d["GNodeId"]
    d["GNodeId"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeId"] = orig_value

    orig_value = d["OwnershipDeedNftId"]
    d["OwnershipDeedNftId"] = 1.1
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["OwnershipDeedNftId"] = orig_value

    orig_value = d["OwnerAddr"]
    d["OwnerAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["OwnerAddr"] = orig_value

    orig_value = d["DaemonAddr"]
    d["DaemonAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["DaemonAddr"] = orig_value

    orig_value = d["GpsPointId"]
    d["GpsPointId"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GpsPointId"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "basegnode.gt"

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d["PrevAlias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["PrevAlias"] = "dw1"

    d["Alias"] = "a.b-h"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["Alias"] = "dw1.iso.me.orange.ta"

    d["GNodeId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GNodeId"] = "9405686a-14fd-4aef-945b-cd7c97903f14"

    d["GpsPointId"] = "d4be12d5-33ba-4f1f-b9e5"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["GpsPointId"] = "50f3f6e8-5937-47c2-8d05-06525ef6467d"

    # End of Test
