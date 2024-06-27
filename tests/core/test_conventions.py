import os, sys
sys.path.append(os.getcwd())
import datetime

import numpy as np
import pytest 

from finstruct.core.conventions import DaycountConvention, TermConvention, RateConvention, CompoundingConvention


@pytest.mark.parametrize("name, value", [(convention.name, convention.value) for convention in DaycountConvention])
class TestDaycountConvention:

    def test_from_key(self, name, value):

        assert DaycountConvention.from_key(name).value == value

    def test_yearfraction(self, name, value):

        dconv = DaycountConvention.from_key(name)
        start_date = np.datetime64(datetime.date(2000,1,1))
        end_date = np.datetime64(datetime.date(2001, 1, 1))
        
        assert round(dconv.calc_yearfraction(start_date, end_date)) == 1.0


@pytest.mark.parametrize("name, value", [(convention.name, convention.value) for convention in TermConvention])
class TestTermConvention:

    def test_from_key(self, name, value):

        assert TermConvention.from_key(name).value == value

    def test_conversion(self, name, value):

        tconv = TermConvention.from_key(name)
        cfunc = tconv.convert(name)
        assert cfunc(1) == 1


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
