import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.conventions import DaycountConvention, TermConvention


class TestDateUnit:
    
    def test_create(self):

        dunit = DateUnit("30/360")
        assert type(dunit) is DateUnit

class TestRateUnit:
    pass

class TestTermUnit:
    pass

def TestUnit():

    tunit = TermUnit("Y", "30/360")
    print(tunit)
    cfuncs = tunit.convert(TermConvention="M")
    print(tunit)
    print(cfuncs['TermConvention'](1))



if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    TestUnit()

