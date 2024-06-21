import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import Unit, TermUnit, RateUnit, DateUnit
from finstruct.driver import Driver


def test_driver():

    unit = TermUnit("D")
    print(repr(unit))
    driver = Driver(unit)
    print(repr(driver))



if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    test_driver()