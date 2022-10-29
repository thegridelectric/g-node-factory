"""create.basegnode.010 type"""

from errors import SchemaError
from schemata.create_basegnode_base import CreateBasegnodeBase


class CreateBasegnode(CreateBasegnodeBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(
                f"Errors making create.basegnode.010 for {self}: {errors}"
            )

    def __repr__(self):
        return "CreateBasegnode"

    def hand_coded_errors(self):
        return []
