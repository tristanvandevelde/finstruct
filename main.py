
from numbers import Number
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style("whitegrid")

from finstruct.core.unit import DateUnit, TermUnit, RateUnit, CashUnit
from finstruct.core.driver import Driver, IRCurveDriver, VOLSurfaceDriver, CalendarDriver
from finstruct.structures.core import Structure, StructArray, Manifold
from finstruct.structures.curve import IRCurve
from finstruct.structures.calendar import Calendar

# driver = IRCurveDriver(
#     Index=[DateUnit("30/360")],
#     Basis=[TermUnit("Y", "30/360")],
#     Projection=[RateUnit("SPOT", "LINEAR", "Y")])

driver = CalendarDriver(name="Calendar",
                        Index=[DateUnit("30/360")],
                        Basis=[],
                        Projection=[CashUnit("PV")])
cal = Calendar.read_csv("data/calendar1.csv", driver, name="MyCalendar")
# curve = Manifold.read_csv("data/treasury_rates.csv", driver, name="Test Manifold")

dates = [np.datetime64(datetime.date(2024,6,18)), np.datetime64(datetime.date(2024,6,14))]

#print(cal.calc_yearfraction(dates[0]))

# fix such that "Date" can also be used directly
#print(cal._data[["Date"]])



print(cal.calc_yearfraction(dates[0]))

# terms = np.arange(1, 31)

# #idx = curve._idx(Date=dates[0], Term=1) # error here
# #idx2 = curve._idx_new(Date=dates[0], Term=10)

# #print(all(idx == idx2))

# index, coords, values = curve._interpolate(Date=dates, Term=terms)
# # print(idx)

# df = pd.DataFrame({"Date": index.flatten(),
#                    "Term": coords.flatten(),
#                    "Rate": values.flatten()})
# print(df)




