import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import Unit, TermUnit, RateUnit, DateUnit


def test_unit():

    pass


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))

