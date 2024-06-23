# """
# File to be used for quick and dirty testing.
# """

# import datetime
# import calendar

# import numpy as np
# import pandas as pd

# from finstruct.unit import TermUnit, RateUnit, DateUnit, DaycountUnit
# from finstruct.structure import Basis, Driver
# from finstruct.curve import IRCurve, IRBaseCurve
# from finstruct.calendar import Calendar

# # coords_unit = [TermUnit("D"), DateUnit(None)]
# # values_unit = RateUnit("SPOT")

# # basis = Basis(coords_unit, values_unit)
# # coords = [(1, np.datetime64("2010-01-01")), 
# #           (10, np.datetime64("2010-01-01")),
# #           (30, np.datetime64("2010-01-01")),
# #           (10, np.datetime64("2010-01-05")),
# #           (30, np.datetime64("2010-01-05")),]
# # values = [0.01, 
# #           0.015,
# #           0.02,
# #           0.015,
# #           0.022]
# # driver = Driver(coords, values, basis)
# # #print(driver.coords)
# # #print(driver.values)


# # # curve = IRCurve(coords, values, basis)
# # #results = driver.filter(term=[1, 10], date=np.datetime64("2010-01-01"))
# # #print(basis.name_coords)
# # #driver.create_grid(term=[1, 10], date=np.datetime64("2010-01-01"))



# # # #interpolator = RegularGridInterpolator(coords, values, method="linear")
# # # #new_vals = interpolator(new_coords)]


# # # if idx.any():
# # #     value = driver.values[idx]
# # # else:
# # #     # interpolate
# # #     pass

# # #driver.get_values(date=[1,2])
# # print(grid)
# # print(conditions)

# # idx = driver.filter(**conditions)
# # print(idx)

# # coords_unit = [TermUnit("D"), DateUnit(None)]
# # values_unit = RateUnit("SPOT")
# # basis = Basis(coords_unit, values_unit)
# # coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
# # values = [0.01, 0.015]
# # curve = Driver(coords, values, basis)
# # result = curve.filter(term=1, date=np.datetime64("2010-01-01"))
# # #result = curve.filter(term=1, date=np.datetime64("2010-01-01"))

# # #result = curve.values[idx]

# # print(result["rate"])
# # #print(list(result))

# curve = IRBaseCurve.read_csv("data/curve1.csv")

# idx = curve.idx(term=[5])
# print(curve.values[idx])

from finstruct.unit import DateUnit, DaycountConvention

#unit = DateUnit("30/360")
#print(unit)
#conv = DaycountConvention.from_key("30/360")
#print(conv)

conv = DaycountConvention.from_key("30/360")
print(conv)
print(conv.name)
print(conv.value)