"""create.basegnode.algo.010 type"""

from errors import SchemaError
from schemata.create_basegnode_algo_base import CreateBasegnodeAlgoBase


class CreateBasegnodeAlgo(CreateBasegnodeAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.basegnode.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateBasegnodeAlgo"

    def hand_coded_errors(self):
        return []
