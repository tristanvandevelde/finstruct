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


    def test_change_YtoM(self):

        tunit = TermUnit("Y", "30/360")
        tunit.convert(TermConvention="M")

        assert tunit.conventions["TermConvention"].value == 1.0
    
    def test_convert_YtoM(self):

        tunit = TermUnit("Y", "30/360")
        cfunc = tunit.convert(TermConvention="M")

        assert cfunc(1) == 12.0


    def test_change_MtoY(self):

        tunit = TermUnit("M", "30/360")
        tunit.convert(TermConvention="Y")

        assert tunit.conventions["TermConvention"].value == 12.0

    def test_convert_MtoY(self):

        tunit = TermUnit("M", "30/360")
        cfunc = tunit.convert(TermConvention="Y")

        assert cfunc(12) == 1.0


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
