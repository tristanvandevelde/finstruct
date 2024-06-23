
import calendar 
from enum import Enum, auto
from types import DynamicClassAttribute

import numpy as np
import numpy.typing as npt

from finstruct.utils.tools import Meta
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



class Unit:

    """Class holding all measurement information about a variable.

    The Unit class is a baseclass, from which other units such as TermUnits and DateUnits are defined.
    It is defined by a number of conventions. Every type of Unit requires a different combination of conventions.

    Attributes
    ----------
    name : str
        Name of the unit.
    dtype : type
        Data type in which the variable will be stored.
    ctypes: list
        List of the convention types which should be used to define the unit.

    Note
    ----
    Ideally, the Unit should function as an Abstract Base Class and should not be used directly.

    """

    name = None
    dtype = None
    ctypes = []
    
    DEFAULTS = {}

    def __init__(self,
                 *args) -> None:
        
        """
        Set all conventions given by input arguments

        Parameters
        ----------
        *args : str
            Arguments representing the (measurement) conventions to be configured.

        """

        self.set_conventions(*args)
        # super().__validate__()

    def __validate__(self):

        # super().__validate__()

        # for convention, ctype in zip(self.conventions.items(), self.ctypes):
        #     TYPECHECK(convention, ctype)
        pass

    def __repr__(self):

        settings = [f"{ctype}({convention.name})" for ctype, convention in self.conventions.items()]
        return f"{self.__class__.__name__}({settings})"


    def set_conventions(self,
                        *args) -> None:
        
        # LENCHECK
        LENCHECK(args, self.ctypes)

        self.conventions = {ctype.__name__: ctype.from_key(convention) for convention, ctype in zip(args, self.ctypes)}

        self.__validate__()

    def convert(self,
                *args) -> callable:
        
        return lambda x: x

    

class DateUnit(Unit):

    name = "Date"
    dtype = "datetime64[D]"
    ctypes = [DaycountConvention]
    DEFAULTS = {"conventions": [DaycountConvention.m_30_360]}

    def __init__(self,
                 daycountconvention) -> None:
        
        super().__init__(daycountconvention)

    def to_numerical(self,
                     value):

        """Returns a numerical value for the date to be used in calculations.
        
        More concretely, the date is converted to a timestamp.
        """

        return calendar.timegm(value.timetuple())


class TermUnit(Unit):

    """Unit describing termstructure.
    
    """

    name = "Term"
    dtype = float
    ctypes = [TermConvention, DaycountConvention]

    def __init__(self,
                 termconvention,
                 daycountconvention) -> None:
        
        super().__init__(termconvention, daycountconvention)

    def convert(self,
                termconvention,
                daycountconvention) -> callable:
        
        termconvention_new = TermConvention.from_key(termconvention)
        daycountconvention_new = DaycountConvention.from_key(daycountconvention)

        if daycountconvention_new != self.conventions[1]:
            raise NotImplementedError
        
        if termconvention_new != self.conventions[0]:
            ## Change expression of term.

            ## For example:
            ## M -> Y x = x/12
            pass
    
class RateUnit(Unit):

    """Unit describing information expressed in (interest) rates.
    """

    name = "Rate"
    dtype = float
    ctypes = [RateConvention, CompoundingConvention]

    def __init__(self,
                 rateconvention,
                 compoundingconvention):
        
        super().__init__(rateconvention, compoundingconvention)

class CashUnit(Unit):

    """Unit to display information expressed in cash exchanges (such as for example price).
    """

    name = "Cash"
    dtype = float
    ctypes = [CashConvention]

    def __init__(self,
                 cashconvention):
        
        super().__init__(cashconvention)


class GenericUnit(Unit):

    """Generic unit to be used in a general setting.

    The generic units allows that the required conventions are determined directly from the constructor,
    and thus do not need to be set before in the class definition.

    Notes
    -----
    For all other documentation, see the base Unit class.
    """

    name = None
    dtype = None
    ctypes = []

    def __init__(self,
                 *args) -> None:
        
        """Create Generic Unit from instantiated Convention objects.

        Parameters
        ----------
        *args: Conventions
            Instances of conventions to be loaded into the unit.
        """
        
        self.ctypes = [type(arg) for arg in args]
        self.conventions = args

