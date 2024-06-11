import pytest 
import os
import sys
sys.path.append(os.getcwd())

import numpy as np

from finstruct.structure import Structure, Space
from finstruct.unit import TermUnit, RateUnit, DateUnit


def test_structure():


    coords_unit = [TermUnit("D"), DateUnit()]
    values_unit = RateUnit("SPOT")
    basis = Space(coords_unit, values_unit)
    coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
    values = [0.01, 0.015]
    struct = Structure(coords, values, basis)
    results = struct.filter(term=1, date=np.datetime64("2010-01-01"))
    #print(results)
    #assert struct.name is not None, ValueError("Struct has no name.")
    assert results is None

if __name__ == "__main__":

    sys.exit(pytest.main(["-c", "tests/pytest.ini"]))


