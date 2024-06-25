from typing import Any

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

class GenericDriver:

    def __init__(self,
                 *args) -> None:
        
        self.__units = zip(np.arange(len(args)), args)

        self.__validate__()

class Driver:

    __SPACE = []

    def __init__(self,
                 *args) -> None:
        
        self.__units = dict(zip(self.__SPACE, args))

        self.__validate__()

    def __validate__(self):

        self.__check_conventions()

    def __repr__(self):

        # for dimension in self.__units:

        #     f""
        
        # return "Driver([{}])".format(*[repr(unit) for unit in self.__basis])
        return "Driver"
    
    
    @property
    def conventions(self):

        return [{unit: list(self.__units[unit].conventions.keys())} for unit in self.__units]
    

    @property
    def ctypes(self):

        # unpack
        conventions = [conv for conv in self.conventions.values()]
        ctypes = set([type(convention) for convention in conventions])

        return ctypes
        

    def __check_conventions(self):

        for ctype in self.ctypes:

            self.conventions

        pass

        # group conventions by type
        # check that values are the same
        # if not return error

        pass

    def convert(self, 
                **kwargs):
        
        """
        Takes in conventions.
        """
        
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
