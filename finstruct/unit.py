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
    DEFAULTS = {
        "convention": None,
        "interpolation": False
    }

    def __init__(self,
                 convention: str,
                 interpolation = False) -> None:
        
        self.convention = convention
        self.interpolation = interpolation


        

    def convert(self,
                convention: str) -> callable:
        
        return True

    def __validate__(self):


        # set defaults
        for key, value in enumerate(self.DEFAULTS):

            if self.key is None:
                self.__setattr__(key, value)

        if self.convention not in list(self.CONVENTIONS):
            raise ValueError("Convention not implemented.")
        
    def __repr__(self):

        return f"{type(self).__name__}(\"{self.type}\")"
    

class DaycountUnit(Unit):

    """
    The DaycountUnit is an abstract unit, used by the DateUnit and the TermUnit.
    It provides the measurements to calculate date differences under different conventions.
    """

    name = "Daycount"
    dtype = None

    CONVENTIONS = (
        "30/360",
        "30/365",
        "ACT/360",
        "ACT/365",
        "ACT/ACT"
    )

    @property
    def fractions(self):

        month, year = self.convention.split("/")

        fractions = {
            "day": 1,
            "month": month,
            "year": year
        }

        return fractions


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

    name = "Term"
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

    name = "Date"
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