"""Base for create.tatradingrights.algo.001 """


import json
from typing import List
from typing import NamedTuple

from errors import SchemaError


class CreateTatradingrightsAlgoBase(NamedTuple):
    TypeName: str = "create.tatradingrights.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if self.TypeName != "create.tatradingrights.algo.001":
            errors.append(
                f"Type requires TypeName of create.tatradingrights.algo.001, not {self.TypeName}."
            )

        return errors
