"""status.basegnode.010 type"""

from errors import SchemaError
from schemata.status_basegnode_base import StatusBasegnodeBase


class StatusBasegnode(StatusBasegnodeBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making status.basegnode.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "StatusBasegnode"

    def hand_coded_errors(self):
        return []
