
import calendar 
from enum import Enum, auto
from types import DynamicClassAttribute

import numpy as np
import numpy.typing as npt

from finstruct.utils.tools import Meta
from finstruct.utils.checks import TYPECHECK

"""
TODO:
    Units to implement:
        - Volatility unit
        - Moneyness unit
        - Money unit
    Rateunit:
        - How to deal with frequency of compounding?
"""

class Convention(Enum):

    """
    Helper class to store the different convention options used in units
    """

    @classmethod
    def from_key(cls,
                 name):
        
        """
        Generate a convention by its namestring.
        """

        for member in cls:
            if member.name == name:
                return member
        return ValueError(f"{name} is not a valid {cls}")

class DaycountConvention(Convention):

    m_30_360 = (30, 360)
    m_30_365 = (30, 365)
    m_ACT_360 = ("ACT", 360)
    m_ACT_365 = ("ACT", 365)
    m_ACT_ACT = ("ACT", "ACT")

    @DynamicClassAttribute
    def name(self):

        """
        Adapt the representation of the names to DAY/YEAR.
        """

        return "/".join([str(x) for x in self.value])
    
    @property
    def fractions(self):

        month, year = self.value
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
            days = np.sum(diff * list(self.fractions.values()))

        return days

    def calc_yearfraction(self,
                          start_date: np.datetime64,
                          end_date: np.datetime64) -> float:
        
        if self.fractions["year"] == "ACT":
            raise NotImplementedError
        else:
            return self.calc_daycount(start_date, end_date)/self.fractions["year"]
    
class TermConvention(Convention):

    M = 1
    Y = 12

class RateConvention(Convention):

    SPOT = auto()
    DISCOUNT = auto()
    FORWARD = auto()

class CompoundingConvention(Convention):

    SIMPLE = auto()
    LINEAR = auto()
    CONTINUOUS = auto()




class Unit:

    name = None
    dtype = None
    ctypes = []
    
    DEFAULTS = {}

    def __init__(self,
                 *args) -> None:
        
        """
        Set all conventions given by input arguments
        """

        self.conventions = np.empty_like(self.ctypes)
        self.set_conventions(*args)

    def __validate__(self):

        # super().__validate__()

        for convention, ctype in zip(self.conventions, self.ctypes):
            TYPECHECK(convention, ctype)

    def __repr__(self):

        return f"{self.__class__}({[convention.name for convention in self.conventions]})"

    def set_conventions(self,
                        *args) -> None:
        
        if not len(args) == len(self.ctypes):
            raise ValueError("Conventions do not match this unit type.")
        
        self.conventions = [ctype.from_key(convention) for convention, ctype in zip(args, self.ctypes)]
        
        self.__validate__()

    def convert(self,
                *args) -> callable:
        
        pass

    

class DateUnit(Unit):

    name = "Date"
    dtype = "datetime64[D]"
    ctypes = [DaycountConvention]

    # DEFAULTS = {
    #     "convention": DaycountConvention.m_30_360
    # }

    def __init__(self,
                 daycountconvention) -> None:
        
        super().__init__(daycountconvention)

    def convert(self,
                daycount) -> callable:
        
        pass

    def to_numerical(self,
                     value):

        """
        Returns a numerical value for the date to be used in calculations.
        More concretely, the date is converted to a timestamp.
        """

        return calendar.timegm(value.timetuple())


class TermUnit(Unit):

    name = "Date"
    dtype = "datetime64[D]"
    ctypes = [TermConvention, DaycountConvention]

    def __init__(self,
                 termconvention,
                 daycountconvention) -> None:
        
        super().__init__(termconvention, daycountconvention)

    def convert(self,
                termconvention,
                daycountconvention) -> callable:
        
        return None
    
class RateUnit(Unit):

    name = "Rate"
    dtype = float
    ctypes = [RateConvention, CompoundingConvention]

    def __init__(self,
                 rateconvention,
                 compoundingconvention):
        
        super().__init__(rateconvention, compoundingconvention)

class GenericUnit(Unit):

    name = None
    dtype = None
    ctypes = []

    def __init__(self,
                 *args) -> None:
        
        self.ctypes = [type(arg) for arg in args]
        super().__init__(*args)




