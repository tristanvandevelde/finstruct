import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.conventions import DaycountConvention, TermConvention, RateConvention, CompoundingConvention



@pytest.mark.parametrize("name, value", [(convention.name, convention.value) for convention in DaycountConvention])
class TestDaycountConvention:

    def test_from_key(self, name, value):

        assert DaycountConvention.from_key(name).value == value



# def test_termconvention():

#     pass

# def test_rateconvention():

#     pass

# def test_compoundingconvention():

#     pass


def test_convention():

    daycount = DaycountConvention.from_key("30/360")
    print(daycount)
    #daycount = DaycountConvention.from_key("ACT/360")
    #print(daycount)
    daycount = daycount.from_key("ACT/360")
    print(daycount)
    #print(daycount)

if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    test_convention()
