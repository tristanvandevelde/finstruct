import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import Unit, TermUnit, RateUnit, DateUnit
from finstruct.core.driver import Driver
from finstruct.utils.checks import TYPECHECK


def test_driver():

    basis = [DateUnit("30/360"), TermUnit("M","30/360")]
    projection = RateUnit("SPOT", "CONTINUOUS", "M")
    d = Driver(basis, projection)

    #unit = TermUnit("D")
    #basis = Basis(unit)

    #assert TYPECHECK(eval(repr(basis)), Basis)

    print(d)
    print(projection)

    #return True


if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    test_driver()
