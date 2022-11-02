"""Tests transfer.tavalidatorcert.algo type, version """
import json

import pytest
from pydantic import ValidationError

from gnf.errors import SchemaError
from gnf.schemata import TransferTavalidatorcertAlgo
from gnf.schemata import TransferTavalidatorcertAlgo_Maker as Maker


def test_transfer_tavalidatorcert_algo_generated():

    d = {
        "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
        "HalfSignedCertTransferMtx": "gqRtc2lng6ZzdWJzaWeSgaJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmConBrxCD8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBqFzxEAEp8UcTEJSyTmgw96/mCnNHKfhkdYMCD5jxWejHRmPCrR8U9z/FBVsoCGbjDTTk2L1k7n/eVlumEk/M1KSe48Jo3RocgKhdgGjdHhuiaRhcGFyhaJhbq9Nb2xseSBNZXRlcm1haWSiYXXZKWh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9tb2xseWNvL3doby13ZS1hcmUvoW3EIItYc29Vmg8xftteXEfMZokX1EDK546h7UFeT4hQQFLZoXQBonVupVZMRFRSo2ZlZc0D6KJmdlGjZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQQ5pG5vdGXEK01vbGx5IEluYyBUZWxlbWV0cnkgU3VydmV5b3JzIGFuZCBQdXJ2ZXlvcnOjc25kxCDHZxhdCT2TxxxZlZ/H5mIku1s4ulDm3EmU6dYKXCWEB6R0eXBlpGFjZmc=",
        "TypeName": "transfer.tavalidatorcert.algo",
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
        validator_addr=gw_tuple.ValidatorAddr,
        half_signed_cert_transfer_mtx=gw_tuple.HalfSignedCertTransferMtx,
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

    orig_value = d["ValidatorAddr"]
    del d["ValidatorAddr"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ValidatorAddr"] = orig_value

    orig_value = d["HalfSignedCertTransferMtx"]
    del d["HalfSignedCertTransferMtx"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["HalfSignedCertTransferMtx"] = orig_value

    ######################################
    # SchemaError raised if attributes have incorrect type
    ######################################

    orig_value = d["ValidatorAddr"]
    d["ValidatorAddr"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["ValidatorAddr"] = orig_value

    orig_value = d["HalfSignedCertTransferMtx"]
    d["HalfSignedCertTransferMtx"] = 42
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["HalfSignedCertTransferMtx"] = orig_value

    ######################################
    # SchemaError raised if TypeName is incorrect
    ######################################

    d["TypeName"] = "not the type alias"
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d)
    d["TypeName"] = "transfer.tavalidatorcert.algo"
