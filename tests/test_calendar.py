import os, sys
sys.path.append(os.getcwd())

import numpy as np
import pytest 

from finstruct.unit import TermUnit, RateUnit, DateUnit
from products.calendar import Calendar


def test_calendar():

    cal = Calendar.read_csv(f"data/config/calendar1.csv")
    assert len(cal.data) == 4


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))

