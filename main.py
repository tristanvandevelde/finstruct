# from finstruct.core.unit import DateUnit, TermUnit
# from finstruct.core.space import Space
# from finstruct.core.driver_new import BaseDriver

from finstruct.core.unit import Unit, DateUnit, TermUnit, RateUnit
from finstruct.utils.types import Meta, FLDict
from finstruct.utils.checks import TYPECHECK

class MetaDriver(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):

        return super().__prepare__(name, bases, **kwargs)
    
    def __new__(metacls, name, bases, namespace, **kwargs):

        for space in kwargs.values():
            TYPECHECK(space, list)
            for el in space:
                if not issubclass(el, Unit):
                    raise ValueError("Only units accepted.")

        namespace = {**namespace,
                     "_SPACES": FLDict(**kwargs)}

        return super().__new__(metacls, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace, **kwargs):

        super().__init__(name, bases, namespace)


## Change such that the kwargs are the names of the spaces
## The values are then the units.

## Can subclass the Metaclass to make MetaBaseDriver and MetaProjectionDriver

## Now require that the init also requests these values.


class C(metaclass=MetaDriver, Basis=[DateUnit, TermUnit], Projection=[RateUnit]):
    
    pass


print(C._SPACES)
