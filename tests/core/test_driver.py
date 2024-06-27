import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.conventions import DaycountConvention, TermConvention
from finstruct.core.driver import Driver

def test_driver():

    #driver = Driver([DateUnit("30/360"), TermUnit("M", "30/360")])
    #driver.print_units()
    #print(driver.conventions)

    #dunit = DateUnit("30/360")

    #print(dunit.conventions)
    #units = driver._units

    print("test")


if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    test_driver()

