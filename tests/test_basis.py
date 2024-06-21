import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import Unit, TermUnit, RateUnit, DateUnit
from finstruct.basis import Basis
from finstruct.utils.checks import TYPECHECK


def test_basis():

    unit = TermUnit("D")
    basis = Basis(unit)

    assert TYPECHECK(eval(repr(basis)), Basis)


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
