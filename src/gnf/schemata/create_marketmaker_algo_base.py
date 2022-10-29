"""Base for create.marketmaker.algo.001 """


import json
from typing import List
from typing import NamedTuple

from errors import SchemaError


class CreateMarketmakerAlgoBase(NamedTuple):
    TypeName: str = "create.marketmaker.algo.001"

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if self.TypeName != "create.marketmaker.algo.001":
            errors.append(
                f"Type requires TypeName of create.marketmaker.algo.001, not {self.TypeName}."
            )

        return errors
