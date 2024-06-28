from finstruct.utils.types import Meta, FLDict
from finstruct.core.unit import DateUnit, TermUnit, RateUnit

class DriverMeta(Meta):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        # kwargs = {}
        #return super().__prepare__(name, bases, **kwargs)
        return super().__prepare__(name, bases)
    
    def __new__(metacls, name, bases, namespace, **kwargs):
        return super().__new__(metacls, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace, **kwargs):

        #namespace = {**namespace,
        #             "_SPACES": FLDict(kwargs["spaces"])}
        print(kwargs)

        super().__init__(name, bases, namespace)

    def __validate__(self):

        """Validate that all the spaces are set correctly."""

        # for dimension in self.spaces:
        #     """
        #     Implement typecheck for Spaces.
        #     """

        pass

    def __new__(cls, name, bases, attrs):
        # for space in attrs['_SPACES']:
        #     attrs[space] = property(SpaceGetter(space), SpaceSetter(space))

        return type.__new__(cls, name, bases, attrs)
    

class Driver(metaclass=DriverMeta):

    @classmethod
    def read_config(cls,
                    configfile):
        pass

class BaseDriver(metaclass=DriverMeta, spaces=["Basis"]):
    pass

class ProjectionDriver(metaclass=DriverMeta, spaces=["Basis", "Projection"]):
    pass

class IRCurveDriver(ProjectionDriver):

    _SPACES["Basis"] = [DateUnit, TermUnit]
    _SPACES["Projection"] = [RateUnit]