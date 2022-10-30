"""create.basegnode.010 type"""

import json
from typing import List
from typing import NamedTuple

from gnf.errors import SchemaError


class CoreGNodeRole100SchemaEnum:
    enum_name: str = "core.g.node.role.100"
    symbols: List[str] = [
        "4502e355",
        "d9823442",
        "0f8872f7",
        "d67e564e",
        "6b58d301",
        "86f21dd2",
        "9521af06",
    ]

    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class CoreGNodeRole100(StrEnum):
    ConductorTopologyNode = auto()
    AtomicTNode = auto()
    TerminalAsset = auto()
    InterconnectionComponent = auto()
    Other = auto()
    MarketMaker = auto()
    AtomicMeteringNode = auto()

    @classmethod
    def values(cls):
        return [elt.value for elt in cls]


class CoreGNodeRoleMap:
    @classmethod
    def type_to_local(cls, symbol):
        if not CoreGNodeRole100SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to CoreGNodeRole100 symbols")
        return cls.type_to_local_dict[symbol]

    @classmethod
    def local_to_type(cls, core_g_node_role):
        if not isinstance(core_g_node_role, CoreGNodeRole100):
            raise SchemaError(f"{core_g_node_role} must be of type {CoreGNodeRole100}")
        return cls.local_to_type_dict[core_g_node_role]

    type_to_local_dict: Dict[str, CoreGNodeRole100] = {
        "4502e355": CoreGNodeRole100.ConductorTopologyNode,
        "d9823442": CoreGNodeRole100.AtomicTNode,
        "0f8872f7": CoreGNodeRole100.TerminalAsset,
        "d67e564e": CoreGNodeRole100.InterconnectionComponent,
        "6b58d301": CoreGNodeRole100.Other,
        "86f21dd2": CoreGNodeRole100.MarketMaker,
        "9521af06": CoreGNodeRole100.AtomicMeteringNode,
    }

    local_to_type_dict: Dict[CoreGNodeRole100, str] = {
        CoreGNodeRole100.ConductorTopologyNode: "4502e355",
        CoreGNodeRole100.AtomicTNode: "d9823442",
        CoreGNodeRole100.TerminalAsset: "0f8872f7",
        CoreGNodeRole100.InterconnectionComponent: "d67e564e",
        CoreGNodeRole100.Other: "6b58d301",
        CoreGNodeRole100.MarketMaker: "86f21dd2",
        CoreGNodeRole100.AtomicMeteringNode: "9521af06",
    }


class CreateBasegnode(NamedTuple):
    TypeName: str = "create.basegnode.010"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if self.TypeName != "create.basegnode.010":
            errors.append(
                f"Type requires TypeName of create.basegnode.010, not {self.TypeName}."
            )

        return errors

    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.basegnode.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateBasegnode"

    def hand_coded_errors(self):
        return []


class CreateBasegnode_Maker:
    type_name = "create.basegnode.010"

    def __init__(self):

        gw_tuple = CreateBasegnode(
            #
        )
        gw_tuple.check_for_errors()
        self.tuple = gw_tuple

    @classmethod
    def tuple_to_type(cls, tuple: CreateBasegnode) -> str:
        tuple.check_for_errors()
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> CreateBasegnode:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> CreateBasegnode:
        new_d = {}
        for key in d.keys():
            new_d[key] = d[key]
        if "TypeName" not in new_d.keys():
            raise SchemaError(f"dict {new_d} missing TypeName")

        gw_tuple = CreateBasegnode(
            TypeName=new_d["TypeName"],
            #
        )
        gw_tuple.check_for_errors()
        return gw_tuple
