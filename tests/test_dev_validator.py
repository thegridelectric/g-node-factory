import pytest

import gnf.config as config
from gnf.dev_utils import DevValidator


@pytest.mark.skip(reason="Skipped so a package can be published")
def test_dev_valdidator_constructor():
    DevValidator(config.ValidatorSettings())
