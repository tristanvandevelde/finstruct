import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import DateUnit, TermUnit
from finstruct.unit import DaycountConvention


def test_unit():

    convention = "30/360"
    conv = DaycountConvention.from_key("30/360")
    #print(conv)
    #print(conv.value)
    assert convention == conv.name


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))

