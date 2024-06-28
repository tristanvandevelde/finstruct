

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
        units[self.name] = value
        return setattr(owner, "_DIMENSIONS", units)

class MetaDriver(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):

        for space in kwargs.values():
            TYPECHECK(space, list)
            for el in space:
                if not issubclass(el, Unit):
                    raise ValueError("Only units accepted.")
                
        spaces = FLDict(**kwargs)

        namespace = {
            **super().__prepare__(name, bases, **kwargs),
            #"__validate__": metacls.__validate__,
            "_DIMTYPES": spaces
        }

        return namespace
    
    def __validate__(self) -> None:

        pass
    
    def __new__(metacls, name, bases, namespace, **kwargs):

        for space in namespace["_DIMTYPES"]:
            namespace[space] = property(SpaceGetter, SpaceSetter)

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



## Can subclass the Metaclass to make MetaBaseDriver and MetaProjectionDriver

class Driver(metaclass=MetaDriver,
             test = [DateUnit]):
    
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
            


class IRCurveDriver(Driver,
                    metaclass=MetaDriver, 
                    Basis=[DateUnit, TermUnit], 
                    Projection=[RateUnit]):
    pass

class CalendarDriver(Driver,
                     metaclass=MetaDriver,
                     Basis=[DateUnit],
                     Projection=[CashUnit]):
    pass

driver = CalendarDriver(Basis=[DateUnit("30/360")], Projection=[TermUnit("Y", "30/360")])

print(driver.Basis)



# def read_config(configfile) -> Driver:

#     # read config file
#     # from general, take attributes
#     # Assert that all spaces are present
#     # Assert that all spaces contain the required units
#     # generate object
#     # return object

#     return True
