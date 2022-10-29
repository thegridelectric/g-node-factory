"""transfer.discoverycert.algo.001 type"""

from errors import SchemaError
from schemata.transfer_discoverycert_algo_base import TransferDiscoverycertAlgoBase


class TransferDiscoverycertAlgo(TransferDiscoverycertAlgoBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making transfer.discoverycert.algo.001 for {self}: {errors}"
            )

    def __repr__(self):
        return "TransferDiscoverycertAlgo"

    def hand_coded_errors(self):
        return []
