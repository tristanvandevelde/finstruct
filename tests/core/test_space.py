import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.space import Space


# @pytest.mark.parametrize("name, value", [(convention.name, convention.value) for convention in DaycountConvention])
# class TestDaycountConvention:

#     def test_from_key(self, name, value):

#         assert DaycountConvention.from_key(name).value == value

def test_space():

    #space = Space(DateUnit("30/360"), TermUnit("M", "30/360"))
    
    #print(space)
    #print(space.conventions)
    #print(space.ctypes)

    #space.convert(DaycountConvention="30/360")
    print("test")

if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    
    test_space()
