import csv
import datetime

import numpy as np
import numpy.typing as npt

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.tools import Meta

from finstruct.unit import DateUnit, MoneyUnit



class Calendar(metaclass=Meta):

    """Calendar class which defines the exchange of cashflows on predetermined times.

    Attributes
    ----------
    dateunit: DateUnit
        Dateunit configuring how the dates of the calendar are interpreted.
    dtypes: np.dtype
        Data types describing how the data is stored.
    data: np.array
        Structured numpy array containing the dates and cashflows.
    """

    DEFAULTS = {
        "dateunit": DateUnit("30/360")
    }

    def __init__(self,
                 dates: npt.ArrayLike,
                 values: npt.ArrayLike,
                 dateunit: DateUnit = None) -> None:
        
        """
        Parameters
        ----------
        dates: npt.ArrayLike
            Dates on which the exchanges happen.
        values: npt.ArrayLike
            Amounts of the exchanges
        """

        self.dateunit = dateunit
        self.dtypes = np.dtype([(self.dateunit.name, self.dateunit.dtype), 
                                ("Amount", float)])
        self.data = np.array(list(zip(dates, values)), dtype=self.dtypes)

        #self.__validate__()
        

    @classmethod
    def read_csv(cls,
                 file,
                 dateunit = None) -> None:
        
        """
        Create Calendar object from a .csv-file.
        """
        
        with open(file=file, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)

        dates = [row["Date"] for row in data]
        values = [row["Cashflow"] for row in data]
        
        return cls(dates, values, dateunit=dateunit)
    
    @property
    def dates(self):

        return self.data[self.dateunit.name]

    @property
    def amounts(self):

        return self.data["Amount"]
    
    # def daycount(self,
    #              start_date: np.datetime64) -> np.array:

    #     return np.array([self.dateunit.conventions[0].calc_daycount(start_date, date) for date in self.dates])

    # def yearfraction(self,
    #                  start_date: np.datetime64) -> np.array:

    #     return np.array([self.dateunit.conventions[0].calc_yearfraction(start_date, date) for date in self.dates])



    