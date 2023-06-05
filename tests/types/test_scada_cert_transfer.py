"""Tests scada.cert.transfer type, version 000"""
import json

import pytest
from gridworks.errors import SchemaError
from pydantic import ValidationError

from gnf.types import ScadaCertTransfer_Maker as Maker


def test_scada_cert_transfer_generated() -> None:
    d = {
        "TaAlias": "d1.iso.me.ghm.orange.ta",
        "SignedProof": "gqNzaWfEQEnByoxlKKnRQkH9QErZguzPXwN9+2FiZNIHIewYLZdIWPQfBKwZxNzdfEc3hdzqPyEKLL/+NlvxL3zR+wGSdgajdHhuiaNhbXTNA+ijZmVlzQPoomZ2GKNnZW6qc2FuZG5ldC12MaJnaMQgfs7M6tXV9AWoJrX3HQ8Fr5ic/1d9kgRAEB7K6bygyJWibHbNBACjcmN2xCCLWHNvVZoPMX7bXlxHzGaJF9RAyueOoe1BXk+IUEBS2aNzbmTEIFXNPyURTCPDClL3PqXp0pKDnZZYSNF0kMAv55W3iS8GpHR5cGWjcGF5",
        "TypeName": "scada.cert.transfer",
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
        ta_alias=gtuple.TaAlias,
        signed_proof=gtuple.SignedProof,
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
    del d2["TaAlias"]
    with pytest.raises(SchemaError):
        Maker.dict_to_tuple(d2)

    d2 = dict(d)
    del d2["SignedProof"]
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

    ######################################
    # SchemaError raised if primitive attributes do not have appropriate property_format
    ######################################

    d2 = dict(d, TaAlias="a.b-h")
    with pytest.raises(ValidationError):
        Maker.dict_to_tuple(d2)

    # End of Test
