import csv
import datetime

import numpy as np
import numpy.typing as npt

from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.utils.types import Meta

from finstruct.core.unit import DateUnit, CashUnit
from finstruct.core.driver import Driver, CalendarDriver
from finstruct.structures.core import Grid
from finstruct.structures.curve import IRCurve

# """
# TODO: Use config files to complement .csv files.
# """

class Calendar(Grid):
    
    _DEFAULTDRIVER = CalendarDriver

    def __init__(self,
                 driver: None,
                 data: None,
                 name: None):
        
        super().__init__(driver=driver, data=data, name=name)

    def __validate__(self):

        pass

    #def calc_npv(self,
    #             curve: IRCurve):
        
    #    timedelta = 

    def calc_yearfraction(self,
                          start_date: np.datetime64) -> np.array:
        

        return np.array([self._driver.Index["Date"].conventions["DaycountConvention"].calc_yearfraction(start_date, date) for date in self._data["Date"]])

    def calc_npv(self,
                 start_date: np.datetime64,
                 curve: IRCurve,
                 daycountconvention = None,
                 frequencyconvention = None):
        
        self.set_conventions(daycount=daycountconvention, frequency=frequencyconvention)
        

        
        
        timedeltas = self.calc_yearfraction(start_date)
        dfactors = curve.get_disc(start_date, timedeltas)

        return sum(dfactors * self._data["Cash"])




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



    
