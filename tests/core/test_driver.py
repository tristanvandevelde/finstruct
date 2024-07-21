import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.conventions import DaycountConvention, TermConvention
from finstruct.core.driver import Driver, IRCurveDriver

class TestDriver:
    pass

class TestIRCurveDriver:

    def test_create(self):

        driver = IRCurveDriver(
            Index=[],
            Basis=[DateUnit("30/360"),TermUnit("Y", "30/360")],
            Projection=[RateUnit("SPOT", "LINEAR", "Y")])
    
        assert type(driver) is IRCurveDriver



if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    #pass
