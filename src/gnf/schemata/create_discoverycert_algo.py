"""create.discoverycert.algo.001 type"""

from errors import SchemaError
from schemata.create_discoverycert_algo_base import CreateDiscoverycertAlgoBase


class CreateDiscoverycertAlgo(CreateDiscoverycertAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.discoverycert.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateDiscoverycertAlgo"

    def hand_coded_errors(self):
        return []
