"""create.ctn.algo.001 type"""

from errors import SchemaError
from schemata.create_ctn_algo_base import CreateCtnAlgoBase


class CreateCtnAlgo(CreateCtnAlgoBase):
    def check_for_errors(self):
        errors = self.derived_errors() + self.hand_coded_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making create.ctn.algo.001 for {self}: {errors}")

    def __repr__(self):
        return "CreateCtnAlgo"

    def hand_coded_errors(self):
        return []
