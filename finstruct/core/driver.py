from typing import Any
from itertools import chain, combinations

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.types import Meta
from finstruct.core.unit import Unit

"""
Driver([Basis], Projection)

TODO:
    - Representation in config files.
    - Make such that all conventions agree with each other.


Make subclasses:
Driver(*args)
StructDriver([Basis],Projection)
EnvDriver([Basis])
    
"""

class MetaDriver(type):

    """
    Create property for each element in the space.
    """



class Driver:

    __SPACE = []

    def __init__(self,
                 *args) -> None:
        
        spaces = (list(args))

        if self.__SPACE:
            self.__units = dict(zip(self.__SPACE, spaces))
        else:
            self.__units = dict(zip(np.arange(len(*args)), spaces))

        # self.__validate__()

    def __validate__(self):

        for space in self.__SPACE:
            self.__check_conventions(space)

    def __repr__(self):

        # for dimension in self.__units:

        #     f""
        
        # return "Driver([{}])".format(*[repr(unit) for unit in self.__basis])
        return "Driver"
    

    def units(self,
              space):

        units = [{unit.name: list(unit.conventions.values())} for unit in list(self.__units[space])]
        
        return units[space]
        
    def conventions(self,
                    space):
        
        conventions = [list(unit.conventions.values()) for unit in list(self.__units[space])]
        conventions = list(chain.from_iterable(conventions))
        #conventions = list(chain(*conventions))

        return conventions
    
    def __check_conventions(self,
                            space):
        
        conventions = self.conventions(space)
        for conv1, conv2 in combinations(conventions, 2):
            if type(conv1) == type(conv2):
                if not conv1.value == conv2.value:
                    raise ValueError("Conventions do not match.")


    def convert(self, 
                **kwargs):
        
        """
        Takes in conventions.
        """
        
        pass

class GenericDriver(Driver):

    pass

class BaseDriver(Driver):

    __SPACE = ["Basis"]

class ProjectionDriver(Driver):

    __SPACE = ["Basis", "Projection"]

    def __init__(self,
                 basis: list,
                 projection: Unit) -> None:
        
        """
        Example
        -------
        Driver([TermUnit("M", "30/360"), DateUnit("30/360|)], RateUnit("SPOT"))
        """
        
        super().__init__(basis, [projection])

    # @property
    # def basis(self):

    #     names = np.array([unit.name for unit in self.__basis])
    #     dtypes = np.dtype([(unit.name, unit.dtype) for unit in self.__basis])

    #     return {"names": names, "dtypes": dtypes}
        
    # @property
    # def projection(self):

    #     name = np.array(self.__projection.name)
    #     dtype = np.dtype([name, self.__projection.dtype])

    #     return {"names": names, "dtypes": dtypes}
