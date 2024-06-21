import datetime
import calendar 

import numpy as np
import numpy.typing as npt

class Unit:

    """
    Class to hold measurement units.
    """

    name = None
    dtype = None
    type = None
    CONVENTIONS = ()
    DEFAULTS = {}

    def __init__(self,
                 convention: str) -> None:
        
        self.set(convention)

    def set(self,
            convention: str) -> None:

        if convention in list(self.CONVENTIONS):
            self.type = convention
        else:
            raise ValueError("Convention not implemented.")
        
    # @property
    # def convention(self) -> set:

    #     return self.type, self.CONVENTIONS[self.type]
    

    def convert(self,
                convention: str) -> callable:
        
        return True

    def __validate__(self):

        for key, value in enumerate(self.DEFAULTS):

            if self.key is None:
                self.__setattr__(key, value)

    def __repr__(self):

        return f"{type(self).__name__}({self.type})"

class DaycountUnit(Unit):

    """
    The DaycountUnit is an abstract unit, used by the DateUnit and the TermUnit.
    It provides the measurements to calculate date differences under different conventions.
    """

    name = "daycount"
    dtype = None

    CONVENTIONS = (
        "30/360",
        "30/365",
        "ACT/360",
        "ACT/365",
        "ACT/ACT"
    )

    def set(self,
            convention: str) -> bool:

        super().set(convention)
        [month, year] = convention.split("/")

        try:
            month = int(month)
        except:
            pass

        try:
            year = int(year)
        except:
            pass

        self.fractions = {
            "day": 1,
            "month": month,
            "year": year
        }


    def calc_daycount(self,
                      start_date: np.datetime64,
                      end_date: np.datetime64) -> int:
        
        if self.fractions["month"] == "ACT":
            days = int(end_date - start_date)
        else:
            get_date = lambda x: np.array([x.day, x.month, x.year])
            start_date = get_date(start_date.astype("object"))
            end_date = get_date(end_date.astype("object"))
            diff = end_date - start_date
            #days = int(np.sum(diff * list(self.fractions.values()), axis=1))
            #print(diff)
            days = np.sum(diff * list(self.fractions.values()))

        return days

    def calc_yearfraction(self,
                          start_date: np.datetime64,
                          end_date: np.datetime64) -> float:
        
        if self.fractions["year"] == "ACT":
            raise ValueError("Not implemented")
        else:
            return self.calc_daycount(start_date, end_date)/self.fractions["year"]

class TermUnit(Unit):

    name = "term"
    dtype = float

    CONVENTIONS = (
        "D",        # daycount
        "Y"         # yearfraction
    )

    def __init__(self,
                 convention: str,
                 daycount: DaycountUnit = None) -> None:
        
        super().__init__(convention)
        self.daycount = daycount


class DateUnit(Unit):

    name = "date"
    dtype = "datetime64[D]"

    CONVENTIONS = [None]

    def __init__(self,
                 convention: str,
                 daycount: DaycountUnit = None) -> None:
        
        super().__init__(convention)
        self.daycount = daycount

    def to_numerical(value):

        """
        Returns a numerical value for the date to be used in calculations.
        More concretely, the date is converted to a timestamp.
        """

        return calendar.timegm(value.timetuple())


        

class RateUnit(Unit):

    name = "rate"
    dtype = float

    CONVENTIONS = (
        "SPOT",
        "FORWARD",
        "DISCOUNTING",
        "ZERO"
    )

# class GenericUnit(Unit):

#     name = None
#     dtype = float

#     CONVENTIONS = {None}

# class MoneynessUnit(Unit):

#     name = "moneyness"
#     dtype = float

# class MoneyUnit(Unit):

#     name = "money"
#     dtype = "f8"

# class VolatilityUnit(Unit):

#     name = "volatility"
#     dtype = float