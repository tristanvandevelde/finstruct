

import configparser
import inspect


from finstruct.core.unit import Unit, DateUnit, TermUnit, RateUnit, CashUnit, MoneynessUnit, VolatilityUnit
from finstruct.utils.types import Meta, FLDict
from finstruct.utils.checks import TYPECHECK
from finstruct.core.space import Space

"""
TODO: implement something like change convention for each dimension.
"""

class SpaceGetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner):
        units = getattr(owner, "_DIMENSIONS")
        return units[self.name]
    
class SpaceSetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner, value):
        units = getattr(owner, "_DIMENSIONS")
        units[self.name] = Space(*value) #value
        return setattr(owner, "_DIMENSIONS", units)

class MetaDriver(type):

    """Metaclass to create Driver classes.
    
    """

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        """Create _DIMTYPES classvariable based on class input.
        """


        dimensions = ["Index", "Basis", "Projection"]
        kwargs = {key: value for key, value in kwargs.items() if key in dimensions}

        for space in kwargs.values():
            TYPECHECK(space, list)
            for el in space:
                if not issubclass(el, Unit):
                    raise ValueError("Only units accepted.")
                
        spaces = FLDict(**kwargs)

        namespace = {
            **super().__prepare__(name, bases, **kwargs),
            "_DIMTYPES": spaces
        }

        return namespace
    
    def __new__(metacls, name, bases, namespace, **kwargs):

        for space in namespace["_DIMTYPES"]:
            namespace[space] = property(SpaceGetter(space), SpaceSetter(space))

        return super().__new__(metacls, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace, **kwargs):

        super().__init__(name, bases, namespace)


class Driver(metaclass=MetaDriver):

    """
    
    """
    
    def __init__(self,
                 name = None,
                 description = None,
                 **kwargs) -> None:
        
        self.name = name
        self.description = description

        if self._DIMTYPES is not None:
            if not set(kwargs.keys()) == set(self._DIMTYPES.keys()):
                raise ValueError("Required dimensions not present.")
            
        self._DIMENSIONS = FLDict(*self._DIMTYPES.keys())

        # Also assert the correct types of units
        for key, value in kwargs.items():  
            for unit in value:
                TYPECHECK(unit, Unit)
            self._DIMENSIONS[key] = Space(*value)

        # self.__validate__()

    def __validate__(self):

        try:
            checkspace = Space(*self._DIMENSIONS["Index"].units, *self._DIMENSIONS["Basis"].units)
            checkspace.__validate__()
        except:
            raise ValueError("Index and Basis are not compatible.")     

    @classmethod
    def read_config(cls,
                    configfile):
        pass

    def write_config(self,
                     configfile):
        pass

    @property
    def units(self):

        """Return all units in all dimensions."""
            


class IRCurveDriver(Driver,
                    metaclass=MetaDriver, 
                    Index=[DateUnit],
                    Basis=[TermUnit], 
                    Projection=[RateUnit]):
    
    """Driver to construct IR Curves.
    
    Dimensions
    ----------
    Index: [DateUnit]
    Basis: [TermUnit]
    Projection: [RateUnit]
    """


class VOLSurfaceDriver(Driver,
                       metaclass=MetaDriver,
                       Index=[DateUnit],
                       Basis=[TermUnit, MoneynessUnit],
                       Projection=[VolatilityUnit]):
    
    """Driver to construct VOL Surfaces.
    
    Dimensions
    ----------
    Index: [DateUnit]
    Basis: [TermUnit, MoneynessUnit]
    Projection: [VolatilityUnit]
    """

class CalendarDriver(Driver,
                     metaclass=MetaDriver,
                     Index=[DateUnit],
                     Basis=[],
                     Projection=[CashUnit]):
    """Driver to construct Calendars.
    
    Dimensions
    ----------
    Basis: Space(DateUnit)
    Projection: Space(CashUnit)
    """