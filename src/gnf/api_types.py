from typing import Dict
from typing import List

from gnf.schemata import CreateCtnAlgo_Maker
from gnf.schemata import CreateTadeedAlgo_Maker
from gnf.schemata import CreateTavalidatorcertAlgo_Maker
from gnf.schemata import ExchangeTadeedAlgo_Maker
from gnf.schemata import HeartbeatA_Maker
from gnf.schemata import TransferTavalidatorcertAlgo_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}

type_makers: List[HeartbeatA_Maker] = [
    CreateCtnAlgo_Maker,
    CreateTadeedAlgo_Maker,
    CreateTavalidatorcertAlgo_Maker,
    HeartbeatA_Maker,
    ExchangeTadeedAlgo_Maker,
    HeartbeatA_Maker,
    TransferTavalidatorcertAlgo_Maker,
]


for maker in type_makers:
    TypeMakerByName[maker.type_name] = maker


def get_api_type_name_list() -> List[str]:
    """Returns the list of TypeNames for the Types that the GNodeRegistry
    uses in its APIs/ABIs. Some of these are types used in asynchronous
    rabbitMQ APIs and/or restful JSON APIs, and some are types used for
    ASA communications.

    The TypeName provides information on encoding/decoding the underlying
    payload in the message, as well as whether that underlying payload
    should be treated initially as bytes or as a string. Each type also
    has a mechanism for being encoded/decoded as a python-native object.

    The TypeNames are strings in left-right-dot format: a collection of words
    separated by periods, where each word except the least significant is
    a string comprised of lower-case alphabetnumeric strings seperated by
    periods, with the most significant word the farthest to the left. The
    final word is a 3-digit number signifying the semantic versioning of
    the type. The maximum length of a TypeRoot ((all but the semantic
    versioning)) is 48.

    Each TypeRoot  is owned by an an account (algo address) and new semantic
    versions must be created by that account and follow certain rules that
    support forwards-and backwards- compatibility for schema evolution.

    The schema for a type is included in the `schematra` subfolder, along
    with the mechanism for encoding/decoding into the python-native object.


    Returns:
        List[str]: The list of TypeNames that the GNodeRegistry uses in
        its APIs/ABIs, in alphabetical order.
    """

    names: List[str] = [
        "create.ctn.algo.001",
        "create.validatorcert.algo.010",
        "create.validatorcert.algo.010",
        "exchange.tadeed.algo.010",
        "heartbeat.a.100",
        "sample.payload.100",
        "transfer.validatorcert.algo.010",
    ]

    names.sort()
    assert set(names) == set(TypeMakerByName.keys())
    return names
