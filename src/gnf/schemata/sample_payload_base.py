"""Base for sample.payload.100"""
import json
from typing import List
from typing import NamedTuple

import algosdk.abi
import property_format
from errors import SchemaError


class SamplePayloadBase(NamedTuple):
    sampleAddr: str
    TypeName: str = "sample.payload.100"

    def __repr__(self):
        r = f"sampleAddr: {self.sampleAddr}"
        return r

    def as_type(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self):
        d = self._asdict()
        return d

    def derived_errors(self) -> List[str]:
        errors = []
        if not isinstance(self.sampleAddr, str):
            errors.append(f"testAddr {self.sampleAddr} must have type str.")
        try:
            property_format.check_is_algo_address_string_format(self.sampleAddr)
        except SchemaError as e:
            errors.append(
                f"testAddr {self.sampleAddr} must have AlgoAddressStringFormat: {e}"
            )
        return errors
