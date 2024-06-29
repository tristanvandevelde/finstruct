

import configparser
import inspect


from finstruct.core.unit import Unit, DateUnit, TermUnit, RateUnit, CashUnit
from finstruct.utils.types import Meta, FLDict
from finstruct.utils.checks import TYPECHECK
from finstruct.core.space import Space


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

class MetaBaseDriver(MetaDriver):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):

        if not list(kwargs.keys()) == ["Basis"]:
            raise KeyError("Only Basis accepted as dimension.")
        
        return super().__prepare__(name, bases, **kwargs)
        

class MetaProjectionDriver(MetaDriver):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):

        if not list(kwargs.keys()) == ["Basis", "Projection"]:
            raise KeyError("Only Basis accepted as dimension.")
        
        return super().__prepare__(name, bases, **kwargs)




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

    @classmethod
    def read_config(cls,
                    configfile):
        pass

    def write_config(self,
                     configfile):
        pass
            


class IRCurveDriver(Driver,
                    metaclass=MetaProjectionDriver, 
                    Basis=[DateUnit, TermUnit], 
                    Projection=[RateUnit]):
    """Driver to construct IR Curves.
    
    Dimensions
    ----------
    Basis: Space(DateUnit, TermUnit)
    Projection: Space(RateUnit)
    """

class CalendarDriver(Driver,
                     metaclass=MetaProjectionDriver,
                     Basis=[DateUnit],
                     Projection=[CashUnit]):
    """Driver to construct Calendars.
    
    Dimensions
    ----------
    Basis: Space(DateUnit)
    Projection: Space(CashUnit)
    """