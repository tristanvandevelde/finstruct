

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

    @classmethod
    def read_config(cls,
                    configfile):
        
        config = configparser.ConfigParser()
        config.read(configfile)

        #general = dict(config["General"].items())
        #print(exec(general["type"] + "()"))

        #TYPECHECK(exec(general["type"]), cls)
        #print(gen)


        space_sections = config.sections().remove("General")

        print(space_sections)

        #general = config.get("General")
        
        ## Extra check: do only if type is subclass of cls
        # -> this way drivers can be read through Driver or through the actual driver (such as IRCurveDriver)

        

    def write_config(self,
                     configfile):

        pass
            



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




def read_config(configfile):
        
    config = configparser.ConfigParser()
    config.read(configfile)

    general = dict(config["General"].items())
    cls = globals()[general["type"]]
    objname = general["name"]
    # check the cls stuff

    #TYPECHECK(exec(general["type"]), Driver)
        #print(gen)


    space_sections = config.sections()
    space_sections.remove("General")
    for section in space_sections:
        print(config[section].name)
        kwargs = dict(config[section].items())
        # unpack somehow
        print()


read_config("config/drivers/IRBaseCurve.ini")
