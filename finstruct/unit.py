import datetime

import numpy as np

class Unit:

    """
    Class to hold measurement units.
    """

    name = None
    dtype = None
    CONVENTIONS = ()
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

    def convert(self,
                convention: str) -> callable:
        
        return True
    
    # @property
    # def type(self):
    #     return self.CONVENTIONS[self.type]


    def validate(self):

        for key, value in enumerate(self.DEFAULTS):

            if self.key is None:
                self.__setattr__(key, value)

class DaycountUnit(Unit):

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
            convention: str) -> None:
        
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
        "D",
        "Y"
    )

    def __init__(self,
                 convention: str,
                 daycount: DaycountUnit = None) -> None:
        
        super().__init__(convention)
        self.daycount = daycount

class DateUnit(Unit):

    name = "date"
    dtype = datetime.date

    def __init__(self):
        pass


        

class RateUnit(Unit):

    name = "rate"
    dtype = float

    CONVENTIONS = (
        "SPOT",
        "FORWARD",
        "DISCOUNTING",
        "ZERO"
    )

class MoneynessUnit(Unit):

    name = "moneyness"
    dtype = float

class VolatilityUnit(Unit):

    name = "volatility"
    dtype = float

class GenericUnit(Unit):

    name = None
    dtype = float

    CONVENTIONS = {None}