"""basegnode.020 type"""

from errors import SchemaError
from schemata.basegnode_base import BasegnodeBase


class Basegnode(BasegnodeBase):
    def check_for_errors(self):
        if self.derived_errors() == []:
            errors = self.hand_coded_errors()
        else:
            errors = self.derived_errors()
        if len(errors) > 0:
            raise SchemaError(f"Errors making basegnode.020 for {self}: {errors}")

    def __repr__(self):
        return "Basegnode"

    def hand_coded_errors(self):
        return []
