"""
File to be used for quick and dirty testing.
"""

import datetime
import calendar

import numpy as np
import pandas as pd

# from finstruct.unit import TermUnit, RateUnit, DateUnit
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

# cal = Calendar.read_csv(f"data/config/calendar1.csv")

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

# def daycount_30_360(date1, date2):
    
#     year_factor = 360
#     month_factor = 30
#     day_factor = 1

#     # we assume that date1 < date2
#     year_diff = date2.year - date1.year
#     month_diff = date2.month - date1.month
#     day_diff = date2.day - date1.day

#     daycount = (year_diff * year_factor) + (month_diff * month_factor) + (day_diff * day_factor)
#     daycount_factor = daycount / year_factor

#     return daycount_factor


# from scipy.interpolate import RegularGridInterpolator

# coords = (1, 2, 3)
# values = 1
# new_coords = (1, 2, 3)


# #interpolator = RegularGridInterpolator(coords, values, method="linear")
# #new_vals = interpolator(new_coords)

# print(cal.data["Date"])

# #data = np.copy(cal.data)
# #print([(datetime.date(point["Date"]) - date1) for point in cal.data])
# print(cal.data.dtype)

# #data = [("2020-01-01", 100), ("2021-01-01", 100)]
# data = ["2020-01-01", "2021-01-01"]

# dates = np.array([(np.datetime64(date), 10) for date in data], dtype=[("Date", "datetime64[D]"), ("Value", "f4")])
# #dates = np.array([(np.datetime64(date)) for date in data], dtype=[("Date", "datetime64[D]")])

# #print(dates.dtype)

# #print(dates[0] - dates[1])
# #test = np.timedelta64(dates[0] - dates[1])
# #print(type(test))
# #days = test.astype("timedelta64[D]")
# #days_fraction = test.astype("timedelta64[D]") / np.timedelta64(1, "D")
# #print(days_fraction)

# print(curve.coords.dtype)
# print(dates.dtype)

# d = dates["Date"]
# print(d[0] - d[1])


# dtype = np.dtype("f4")
# name = "amount"

# np.array([10, 20, 30], dtype=(name, dtype))

# types = np.dtype([("date", "datetime64[D]"), ("amount", "f4")])
# values = [("2020-01-01", 10)]
# arr = np.array(values, dtype=types)
# values2 = [(datetime.date(2020,1,1), 10)]
# arr2 = np.array(values, dtype=types)


# diff = arr2["date"] - eval_date


cal = Calendar.read_csv("data/config/calendar1.csv")
eval_date = np.datetime64("2000-01-01", "D")
#diff = (cal.data["date"] - eval_date).astype("timedelta64[ns]")
#print(diff.astype("timedelta64[M]"))

#print(cal.data["date"].astype("datetime64[M]") - eval_date.astype("datetime64[M]"))

#df = pd.DataFrame(cal.data).dtypes
#print(df["date"].dt.day)

import time

tic = time.time()
dti_cf = pd.to_datetime(cal.data["date"])
dti_eval = pd.to_datetime(eval_date)

day_diff = dti_cf.day - dti_eval.day
month_diff = dti_cf.month - dti_eval.month
year_diff = dti_cf.year - dti_eval.year

daycount = year_diff*360 + month_diff*30 + day_diff
print(np.array(daycount/360))
toc = time.time()

print(f"Using pandas: {toc-tic}")

tic = time.time()
dates = np.array([(date.day, date.month, date.year) for date in cal.data["date"].astype("object")])
eval_date = eval_date.astype("object")
diff = dates - [eval_date.day, eval_date.month, eval_date.year]
fractions = [1, 30, 360]
# 30 / 360

print(np.sum(diff * fractions, axis=1)/360)
toc = time.time()
print(f"Using pure python: {toc-tic}")

# pure Python is 8.5 times faster