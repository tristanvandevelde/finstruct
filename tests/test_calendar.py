import os, sys
sys.path.append(os.getcwd())
import datetime

import numpy as np
import pytest 

from finstruct.unit import TermUnit, RateUnit, DateUnit, DaycountUnit
from finstruct.calendar import Calendar


def test_calendar():



    dcunit = DaycountUnit("30/360")
    dunit = DateUnit(None, dcunit)
    cal = Calendar.read_csv("data/config/calendar1.csv", dateunit=dunit)

    eval_date_1 = np.datetime64(datetime.date(2000,1,1), "D")
    eval_date_2 = np.datetime64(datetime.date(2010,1,1), "D")

    assert cal.get_npv(eval_date_1) < cal.get_npv(eval_date_2) 


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))

