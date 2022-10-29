"""Base for create.basegnode.010 """


import json
from typing import List
from typing import NamedTuple

from errors import SchemaError


class CreateBasegnodeBase(NamedTuple):
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