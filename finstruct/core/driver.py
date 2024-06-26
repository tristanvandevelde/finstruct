# from typing import Any
from itertools import chain, combinations

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.types import Meta
from finstruct.core.unit import Unit
from finstruct.core.space import Space

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

"""
Adapt getters & setters to work with lists rather than Spaces.
"""

class SpaceGetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner):

        # units = [{unit.name: list(unit.conventions.values())} for unit in list(self.__units[space])]
        # return units[space]

        units = getattr(owner, "_dimensions")
        return units[self.name]
    
class SpaceSetter(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, owner, value):
        units = getattr(owner, "_dimensions")
        units[self.name] = value
        return setattr(owner, "_dimensions", units)
    



class DriverMeta(Meta):

    def __new__(cls, name, bases, attrs):
        for space in attrs['_SPACES']:
            attrs[space] = property(SpaceGetter(space), SpaceSetter(space))

        return type.__new__(cls, name, bases, attrs)
    



class Driver(metaclass=DriverMeta):

    _SPACES = ['Basis', 'Projection']

    def __init__(self, *args) -> None:

        spaces = [Space(*unitlist) for unitlist in args]

        if self._SPACES:
            self._dimensions = dict(zip(self._SPACES, spaces))
        else: 
            # if no spaces are provided, properties will also not be created
            self._dimensions = dict(zip(np.arange(len(*args)), spaces))

    def __validate__(self):

        for space in self._dimensions.values():
            TYPECHECK(space, Space)


    def __repr__(self):

        #         # return "Driver([{}])".format(*[repr(unit) for unit in self.__basis])
        ## Adapt representation to work with lists.
        pass




class BaseDriver(Driver):

    _SPACES = ["Basis"]

    def __init__(self,
                 basis: list) -> None:
        
        super().__init__(basis)

class ProjectionDriver(Driver):

    _SPACES = ["Basis", "Projection"]

    def __init__(self,
                 basis: list,
                 projection: Unit) -> None:
        
        super().__init__(basis, [projection])

        ## TODO: Make sure interpolation only happens on the basis, and is disallowed for non numeric units.

