"""create.tatradingrights.algo.001 type"""

from errors import SchemaError
from schemata.create_tatradingrights_algo_base import CreateTatradingrightsAlgoBase


class CreateTatradingrightsAlgo(CreateTatradingrightsAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.tatradingrights.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateTatradingrightsAlgo"

    def hand_coded_errors(self):
        return []
