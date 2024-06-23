from typing import Any

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.tools import Meta
from finstruct.unit import Unit

"""
Driver([Basis], Projection)
"""

class Driver:

    """Driver class to hold the combination of Units to 'drive' the Structures.

    Attributes
    ----------
    basis: np.array(Units)
        Coordinate driving units
    projection: Unit
        Value driving unit
    
    """

    def __init__(self,
                 basis: list,
                 projection) -> None:
        
        """
        Example
        -------
        Driver([TermUnit("M", "30/360"), DateUnit("30/360|)], RateUnit("SPOT"))
        """
        
        self.__basis = basis
        self.__projection = projection

    def __validate__(self) -> None:

        # Make sure everything is a unit
        # Check dimensions
        # Make sure all units are consistent with each other

        raise ValueError
    
    def convert(self,
                **kwargs) -> callable:
        
        return lambda x: x

    @property
    def basis(self):

        names = np.array([unit.name for unit in self.__basis])
        dtypes = np.dtype([(unit.name, unit.dtype) for unit in self.__basis])

        return (names, dtypes)
        
    @property
    def projection(self):

        name = np.array(self.__projection.name)
        dtype = np.dtype([name, self.__projection.dtype])

        return (name, dtype)

    def __repr__(self):
        
        return "Driver([{}])".format(*[repr(unit) for unit in self.__basis])
    



