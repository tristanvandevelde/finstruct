import datetime
import calendar 

import numpy as np

class Unit:

    """
    Class to hold measurement units.
    """

    name = None
    dtype = None
    type = None
    CONVENTIONS = {}
    DEFAULTS = {}

    def __init__(self,
                 convention: str) -> None:
        
        self.set(convention)

    def set(self,
            convention: str) -> None:
        
        """
        
        """

        if convention in list(self.CONVENTIONS):
            self.type = convention
        else:
            raise ValueError("Convention not implemented.")
        
    @property
    def convention(self) -> set:

        return self.type, self.CONVENTIONS[self.type]

    def convert(self,
                convention: str) -> callable:
        
        return True

    def validate(self):

        for key, value in enumerate(self.DEFAULTS):

            if self.key is None:
                self.__setattr__(key, value)

class DaycountUnit(Unit):

    """
    The DaycountUnit is an abstract unit, used by the DateUnit and the TermUnit.
    It provides the measurements to calculate date differences under different conventions.
    """

    name = "daycount"
    dtype = str

    CONVENTIONS = (
        "30/360",
        "30/365",
        "ACT/360",
        "ACT/365",
        "ACT/ACT"
    )

    def set(self,
            convention: str) -> bool:
        
        """
        Set the convention of the unit and convert.

        Parameters
        ----------
        convention: string
            Convention to which to convert the Unit

        Raises
        ------
        Exception
            convention must be implemented

        Returns
        -------
        bool
            Information code if the conversion has been correctly executed.

        Example
        -------

        unit.convert("30/360")

        """


        
        super().set(convention)
        [measure, base] = convention.split("/")
        try:
            self.measure = int(measure)
        except:
            self.measure = measure
        try:
            self.base = int(base)
        except:
            self.base = base

    def daycount(self,
                 start_date: datetime.date,
                 end_date: datetime.date) -> int:
        
        pass

    def yearfraction(self,
                     start_date: datetime.date,
                     end_date: datetime.date) -> float:
        
        pass

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
    dtype = "timedelta64[D]"

    def __init__(self):
        pass

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

# class VolatilityUnit(Unit):

#     name = "volatility"
#     dtype = float