"""
File to be used for quick and dirty testing.
"""

import datetime
import calendar

import numpy as np
import pandas as pd

from finstruct.unit import TermUnit, RateUnit, DateUnit, DaycountUnit
from finstruct.structure import Basis, Driver
# from finstruct.curve import IRCurve
from finstruct.calendar import Calendar

# coords_unit = [TermUnit("D"), DateUnit(None)]
# values_unit = RateUnit("SPOT")

# basis = Basis(coords_unit, values_unit)
# coords = [(1, np.datetime64("2010-01-01")), 
#           (10, np.datetime64("2010-01-01")),
#           (30, np.datetime64("2010-01-01")),
#           (10, np.datetime64("2010-01-05")),
#           (30, np.datetime64("2010-01-05")),]
# values = [0.01, 
#           0.015,
#           0.02,
#           0.015,
#           0.022]
# driver = Driver(coords, values, basis)
# #print(driver.coords)
# #print(driver.values)


# # curve = IRCurve(coords, values, basis)
# #results = driver.filter(term=[1, 10], date=np.datetime64("2010-01-01"))
# #print(basis.name_coords)
# #driver.create_grid(term=[1, 10], date=np.datetime64("2010-01-01"))



# #print(np.array(driver.coords))
# #print(np.isin(driver.coords, (1, np.datetime64("2010-01-01", "D"))))

# # #interpolator = RegularGridInterpolator(coords, values, method="linear")
# # #new_vals = interpolator(new_coords)]


# #print(driver.coords.dtype.names)
# dates = [np.datetime64(datetime.date(2010,1,1)), np.datetime64(datetime.date(2010,1,5))]
# terms = [1, 10, 30]
# grid = driver.create_grid(dates, terms)
# conditions = dict(zip(["date", "term"], grid.T))

# # if idx.any():
# #     value = driver.values[idx]
# # else:
# #     # interpolate
# #     pass

# #driver.get_values(date=[1,2])
# print(grid)
# print(conditions)

# idx = driver.filter(**conditions)
# print(idx)

coords_unit = [TermUnit("D"), DateUnit(None)]
values_unit = RateUnit("SPOT")
basis = Basis(coords_unit, values_unit)
coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
values = [0.01, 0.015]
curve = Driver(coords, values, basis)
result = curve.filter(term=1, date=np.datetime64("2010-01-01"))
#result = curve.filter(term=1, date=np.datetime64("2010-01-01"))

#result = curve.values[idx]

print(result["rate"])
#print(list(result))