import csv
import datetime

import numpy as np
import numpy.typing as npt

from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.utils.tools import Meta

from finstruct.unit import DateUnit, CashUnit



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
        "dateunit": DateUnit("30/360"),
        "cashunit": CashUnit("EUR")
    }

    def __init__(self,
                 dates: npt.ArrayLike,
                 values: npt.ArrayLike,
                 dateunit: DateUnit = None,
                 cashunit: CashUnit = None) -> None:
        
        """
        Parameters
        ----------
        dates: npt.ArrayLike
            Dates on which the exchanges happen.
        values: npt.ArrayLike
            Amounts of the exchanges
        """

        self.dateunit = dateunit
        self.cashunit = cashunit
        LENCHECK(dateunit, cashunit)
        self.dtypes = np.dtype([(self.dateunit.name, self.dateunit.dtype), 
                                (self.cashunit.name, self.cashunit.dtype)])
        self.data = np.array(list(zip(dates, values)), dtype=self.dtypes)        

    @classmethod
    def read_csv(cls,
                 file,
                 dateunit = None) -> None:
        
        """Create Calendar object from a .csv-file.

        Parameters
        ----------
        file: str
            Location of the .csv-file.
        dateunit: DateUnit (optional)
            DateUnit to be used in the Calendar.

        Notes
        -----
        The .csv-file is expected to have the following headers: Date, Cashflow.
        """
        
        with open(file=file, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)

        dates = [row["Date"] for row in data]
        values = [row["Cashflow"] for row in data]
        
        return cls(dates, values, dateunit=dateunit)
    
    @property
    def dates(self):

        """Return the dates of the calendar.
        """

        return self.data[self.dateunit.name]

    @property
    def amounts(self):

        """Return the amounts of the calendar.
        """

        return self.data[self.cashunit.name]
    
    def daycount(self,
                 start_date: np.datetime64) -> np.array:
        
        """Calculate the daycount array for a given starting date.
        """

        return np.array([self.dateunit.conventions["DaycountConvention"].calc_daycount(start_date, date) for date in self.dates])

    def yearfraction(self,
                     start_date: np.datetime64) -> np.array:
        
        """Calculate the yearfraction array for a given starting date.
        """

        return np.array([self.dateunit.conventions["DaycountConvention"].calc_yearfraction(start_date, date) for date in self.dates])



    