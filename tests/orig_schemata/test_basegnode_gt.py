"""Tests basegnode.gt type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.errors import SchemaError
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker as Maker


def test_basegnode_gt_generated():

    d = {
        "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
        "Alias": "d1",
        "StatusGtEnumSymbol": "153d3475",
        "RoleGtEnumSymbol": "00000000",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "PrevAlias": "d",
        "TypeName": "basegnode.gt",
        "Version": "020",
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

    d2 = dict(d)
    del d2["TypeName"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["GNodeId"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["Alias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["StatusGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["RoleGtEnumSymbol"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["GNodeRegistryAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    ######################################
    # Optional attributes can be removed from type
    ######################################

    d2 = dict(d)
    if "GpsPointId" in d2.keys():
        del d2["GpsPointId"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "OwnershipDeedNftId" in d2.keys():
        del d2["OwnershipDeedNftId"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "OwnershipDeedValidatorAddr" in d2.keys():
        del d2["OwnershipDeedValidatorAddr"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "PrevAlias" in d2.keys():
        del d2["PrevAlias"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "OwnerAddr" in d2.keys():
        del d2["OwnerAddr"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "DaemonAddr" in d2.keys():
        del d2["DaemonAddr"]
    Maker.dict_to_tuple(d2)

    d2 = dict(d)
    if "TradingRightsNftId" in d2.keys():
        del d2["TradingRightsNftId"]
    Maker.dict_to_tuple(d2)

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    d2 = dict(d, StatusGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).Status = GNodeStatus.default()

    d2 = dict(d, RoleGtEnumSymbol="hi")
    Maker.dict_to_tuple(d2).Role = CoreGNodeRole.default()

    d2 = dict(d, OwnershipDeedNftId="5.1")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, TradingRightsNftId="1.1")
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

    d2 = dict(d, GNodeId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, Alias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, GpsPointId="d4be12d5-33ba-4f1f-b9e5")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d, PrevAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
