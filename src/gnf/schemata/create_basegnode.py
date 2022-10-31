"""create.basegnode.010 type"""

import json
from typing import List
from typing import NamedTuple

from gnf.errors import SchemaError


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
