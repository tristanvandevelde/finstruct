import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import TermUnit, RateUnit, DateUnit
#from finstruct.structure import Structure, Basis


def test_structure():

    # coords_unit = [TermUnit("D"), DateUnit(None)]
    # values_unit = RateUnit("SPOT")
    # basis = Basis(coords_unit, values_unit)
    # coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
    # values = [0.01, 0.015]
    # curve = Structure(coords, values, basis)
    # results = curve.filter(term=1, date=np.datetime64("2010-01-01"))
    
    # assert results is not None

    return True

if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))