"""create.terminalasset.algo.010 type"""

from errors import SchemaError
from schemata.create_terminalasset_algo_base import CreateTerminalassetAlgoBase


class CreateTerminalassetAlgo(CreateTerminalassetAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.terminalasset.algo.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateTerminalassetAlgo"

    def hand_coded_errors(self):
        return []
