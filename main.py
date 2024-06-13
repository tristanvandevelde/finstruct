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

coords_unit = [TermUnit("D"), DateUnit(None)]
values_unit = RateUnit("SPOT")

basis = Basis(coords_unit, values_unit)
coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
values = [0.01, 0.015]
driver = Driver(coords, values, basis)
#print(driver.coords)
#print(driver.values)


# curve = IRCurve(coords, values, basis)
#results = driver.filter(term=[1, 10], date=np.datetime64("2010-01-01"))
#print(basis.name_coords)
#driver.create_grid(term=[1, 10], date=np.datetime64("2010-01-01"))
x = [1, 10]
y = ["a", "b"]

grid = np.meshgrid(x, y, indexing='ij')

arr = np.array(grid).reshape(2,-1).T
newarr = np.core.records.fromarrays(arr.transpose())
newarr = np.array(newarr, dtype=[("x",float),("y",str)])

print(np.array(driver.coords))
#print(np.isin(driver.coords, (1, np.datetime64("2010-01-01", "D"))))

# #interpolator = RegularGridInterpolator(coords, values, method="linear")
# #new_vals = interpolator(new_coords)]

#unstructured = np.lib.recfunctions.structured_to_unstructured(driver.coords)
#print(unstructured)

#from numpy.lib.recfunctions import structured_to_unstructured
#print(structured_to_unstructured(driver.coords))

print(driver.coords.dtype.names)

