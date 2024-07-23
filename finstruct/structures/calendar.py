import csv
import datetime

import numpy as np
import numpy.typing as npt

from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.utils.types import Meta

from finstruct.core.unit import DateUnit, CashUnit
from finstruct.core.driver import Driver, CalendarDriver
from finstruct.structures.core import Grid

# """
# TODO: Use config files to complement .csv files.
# """

class Calendar(Grid):
    
    _DEFAULTDRIVER = CalendarDriver



# class Calendar:

#     """Calendar class which defines the exchange of cashflows on predetermined times.

#     Attributes
#     ----------
#     dateunit: DateUnit
#         Dateunit configuring how the dates of the calendar are interpreted.
#     dtypes: np.dtype
#         Data types describing how the data is stored.
#     data: np.array
#         Structured numpy array containing the dates and cashflows.
#     """

#     DEFAULTS = {
#         "driver": Driver([DateUnit("30/360")],[CashUnit("EUR")])
#     }

#     def __init__(self,
#                  dates: npt.ArrayLike,
#                  values: npt.ArrayLike,
#                  driver: Driver = None) -> None:
        
#         """
#         Parameters
#         ----------
#         dates: npt.ArrayLike
#             Dates on which the exchanges happen.
#         values: npt.ArrayLike
#             Amounts of the exchanges
#         """

#         self.name = None
#         self.date = None
#         self.driver = None

#         # self.dtypes = np.dtype([(self.dateunit.name, self.dateunit.dtype), 
#         #                         (self.cashunit.name, self.cashunit.dtype)])
#         # self.data = np.array(list(zip(dates, values)), dtype=self.dtypes)        

    
#     @property
#     def dates(self):

#         """Return the dates of the calendar.
#         """

#         return self.data[self.dateunit.name]

#     @property
#     def amounts(self):

#         """Return the amounts of the calendar.
#         """

#         return self.data[self.cashunit.name]
    
#     def daycount(self,
#                  start_date: np.datetime64) -> np.array:
        
#         """Calculate the daycount array for a given starting date.
#         """

#         return np.array([self.dateunit.conventions["DaycountConvention"].calc_daycount(start_date, date) for date in self.dates])

#     def yearfraction(self,
#                      start_date: np.datetime64) -> np.array:
        
#         """Calculate the yearfraction array for a given starting date.
#         """

#         return np.array([self.dateunit.conventions["DaycountConvention"].calc_yearfraction(start_date, date) for date in self.dates])



    
