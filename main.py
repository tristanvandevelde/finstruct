"""
File to be used for quick and dirty testing.
"""

import datetime
import calendar

import numpy as np
import pandas as pd

from finstruct.unit import TermUnit, RateUnit, DateUnit, DaycountUnit
# from finstruct.structure import Basis, Driver
# from finstruct.curve import IRCurve
from finstruct.calendar import Calendar

# coords_unit = [TermUnit("D"), DateUnit()]
# values_unit = RateUnit("SPOT")

# basis = Basis(coords_unit, values_unit)
# coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
# values = [0.01, 0.015]
# curve = IRCurve(coords, values, basis)
# results = curve.filter(term=1, date=np.datetime64("2010-01-01"))


# date1 = datetime.date(2000, 1, 1)
# date2 = datetime.date(2010, 1, 1)

# print((date2 - date1).days)
# print(np.datetime64(date2) - np.datetime64(date1))
# print(date1.year)

# date3 = np.datetime64(date2)
# # if is numpy
# print(date3.astype(datetime.date))

# print(date2 > date1)

# def daycount_act_act(date1, date2):

#     # we assume that date1 < date2
#     leap_years = [y for y in range(date1.year, date2.year) if calendar.isleap(y)]
#     leap_periods = [[dates, dates], [dates, dates]]
#     nonleap_periods = [[dates_dates], [dates, dates]]






# #interpolator = RegularGridInterpolator(coords, values, method="linear")
# #new_vals = interpolator(new_coords)



dcunit = DaycountUnit("30/360")
dunit = DateUnit(None, dcunit)
cal = Calendar.read_csv("data/config/calendar1.csv", dateunit=dunit)

eval_date = np.datetime64("2000-01-01", "D")
npv = cal.get_npv(eval_date)

print(npv)