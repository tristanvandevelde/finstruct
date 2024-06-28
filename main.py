# from finstruct.core.unit import DateUnit, TermUnit
# from finstruct.core.space import Space
# from finstruct.core.driver_new import BaseDriver

from finstruct.core.unit import Unit, DateUnit, TermUnit, RateUnit
from finstruct.utils.types import Meta, FLDict
from finstruct.utils.checks import TYPECHECK

import inspect

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
            "__validate__": metacls.__validate__,
            "_DIMTYPES": spaces
        }

        return namespace
    
    def __validate__(self) -> None:

        pass
    
    def __new__(metacls, name, bases, namespace, **kwargs):

        for space in namespace["_DIMTYPES"]:
            namespace[space] = property(SpaceGetter, SpaceSetter)

        print(inspect.signature(namespace["__init__"]))
        print(list(namespace["_DIMTYPES"].keys()))

        return super().__new__(metacls, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace, **kwargs):

        super().__init__(name, bases, namespace)


## Change such that the kwargs are the names of the spaces
## The values are then the units.

## Can subclass the Metaclass to make MetaBaseDriver and MetaProjectionDriver

## Now require that the init also requests these values.


class IRCurveDriver(metaclass=MetaDriver, Basis=[DateUnit, TermUnit], Projection=[RateUnit]):
    
    def __init__(self,
                 basis,
                 projection):
        pass



print(IRCurveDriver._DIMTYPES)

#inspect()
