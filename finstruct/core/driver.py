# from typing import Any
from itertools import chain, combinations

import numpy as np

# from finstruct.utils.checks import TYPECHECK
from finstruct.utils.types import Meta
# from finstruct.core.unit import Unit

# """
# Driver([Basis], Projection)

# TODO:
#     - Representation in config files.
#     - Make such that all conventions agree with each other.


# Make subclasses:
# Driver(*args)
# StructDriver([Basis],Projection)
# EnvDriver([Basis])
    
# """
"""
Idea: Extend over 2 classes. 
A Driver can consist of multiple Spaces.
Each Space needs to be internally consistent.
"""


## Maybe also implement getters & setters for the conventions




class SpaceGetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner):

        # units = [{unit.name: list(unit.conventions.values())} for unit in list(self.__units[space])]
        # return units[space]

        units = getattr(owner, "_units")
        return units[self.name]
    
class SpaceSetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner, value):
        units = getattr(owner, "_units")
        units[self.name] = value
        return setattr(owner, "_units", units)
    
#     # @property
#     # def basis(self):

#     #     names = np.array([unit.name for unit in self.__basis])
#     #     dtypes = np.dtype([(unit.name, unit.dtype) for unit in self.__basis])

#     #     return {"names": names, "dtypes": dtypes}
        
#     # @property
#     # def projection(self):

#     #     name = np.array(self.__projection.name)
#     #     dtype = np.dtype([name, self.__projection.dtype])

#     #     return {"names": names, "dtypes": dtypes}


class DriverMeta(Meta):

    def __new__(cls, name, bases, attrs):
        for space in attrs['_SPACES']:
            attrs[space] = property(SpaceGetter(space), SpaceSetter(space))

        return type.__new__(cls, name, bases, attrs)
    
class Driver(metaclass=DriverMeta):

    _SPACES = ['Basis', 'Projection']

    def __init__(self, *args) -> None:


        if self._SPACES:
            self._units = dict(zip(self._SPACES, list(args)))
        else: 
            # if no spaces are provided, properties will also not be created
            self._units = dict(zip(np.arange(len(*args)), list(args)))

    def __validate__(self):

        for space in self._SPACES:
            #self._check_conventions(space)
            return True

    def __repr__(self):

        #         # return "Driver([{}])".format(*[repr(unit) for unit in self.__basis])
        return "Driver"










# class BaseDriver(Driver):

#     __SPACE = ["Basis"]

# class ProjectionDriver(Driver):

#     __SPACE = ["Basis", "Projection"]

#     def __init__(self,
#                  basis: list,
#                  projection: Unit) -> None:
        
#         """
#         Example
#         -------
#         Driver([TermUnit("M", "30/360"), DateUnit("30/360|)], RateUnit("SPOT"))
#         """
        
#         super().__init__(basis, [projection])


