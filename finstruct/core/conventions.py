"""CONVENTIONS MODULE
"""

import calendar 
from enum import Enum, auto
from types import DynamicClassAttribute

import numpy as np
import numpy.typing as npt

from finstruct.utils.checks import TYPECHECK, LENCHECK

"""
TODO:
    Units to implement:
        - Volatility unit
        - Moneyness unit
        - Money unit
        - Rate unit
    Rateunit:
        - How to deal with frequency of compounding?
    To implement:
        - Conversion methods
"""

class Convention(Enum):

    """Helper class to store the different convention options used in Units.

    Attributes
    ----------
    - cname: str
        Name of the convention type.
    - name: str
        Name of the convention.
    - value: Any
        Representation of the convention.

    """

    @classmethod
    def from_key(cls,
                 name):
        
        """Generate a convention by its namestring.
        

        Parameters
        ----------
        name: str
            Name of the convention to be set.

        Returns
        -------
        conv: Convention
            Created instance of the Convetion class.

        Raises
        ------
        ValueError
            If the name is not defined in the Convention.
        """

        for member in cls:
            if member.name == name:
                return member
            
        raise ValueError(f"{name} is not a valid {cls}")

class DaycountConvention(Convention):

    _cname = "Daycount"

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
        
        """Calculate the daycount between two dates.
        """
         
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
        
        """Calculate the yearfraction between two dates.
        """
        
        if self.fractions["year"] == "ACT":
            raise NotImplementedError
        else:
            return self.calc_daycount(start_date, end_date)/self.fractions["year"]
    
class TermConvention(Convention):

    D = 0
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

class CashConvention(Convention):

    EUR = auto()
    USD = auto()


