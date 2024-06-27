import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.space import Space

class TestSpace:

    def test_create_success(self):

        dunit = DateUnit("30/360")
        tunit = TermUnit("Y", "30/360")
        space = Space(dunit, tunit)

        assert type(space) == Space

    def test_create_fail(self):

        dunit = DateUnit("30/360")
        tunit = TermUnit("Y", "30/365")
        with pytest.raises(ValueError):
            space = Space(dunit, tunit)


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    