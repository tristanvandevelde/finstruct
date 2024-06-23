import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import DateUnit, TermUnit
from finstruct.unit import DaycountConvention, TermConvention

def test_daycountconvention():
    
    convention = "30/360"
    conv = DaycountConvention.from_key("30/360")
    assert convention == conv.name


def test_unit():

    dunit = DateUnit("30/360")
    func = dunit.convert("30/365")
    assert 1 == func(1)


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))

