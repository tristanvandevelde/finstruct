

from abc import ABCmeta

import numpy as np
import numpy.typing as npt

from finstruct.structures.structure import StructArray
## TODO: move StructArray to tools

"""
Basic Python implementation of interpolation functionality.
Allows for the comparison and benchmarking of C++ implementation.
"""

class Interpolation(metaclass=ABCmeta):

    def __init__(self,
                 index: StructArray,
                 coords: StructArray,
                 values: StructArray):
        
        # replace by pointers
        self.index = index
        self.coords = coords
        self.values = values

        self.intrapolate = True
        self.extrapolate = False

    def construct(self):

        """
        Construct the required parameter values such that the evaluate function can be executed.
        """

    def evaluate(self,
                 coord):
        
        pass

    def __call__(self,
                 coords: npt.ArrayLike):
        
        """
        Evaluate the interpolation.

        Parameters
        ----------
        coords: array_like[T,n]
                points to evaluate

        Returns
        -------
        values: array_like[n]
                interpolated values 
        """
        
        values = np.empty(len(coords))
        it = np.nditer([coords, values], flags=["f_index"])
        for coords, values in it:
            values[it.index] = self.evaluate(coords)
        
        return values


## Use decorator to make classes of Interpolations

class Interpolation(metaclass=ABCmeta):

    def __init__(self,
                 index: StructArray,
                 coords: StructArray,
                 values: StructArray):
        
        # replace by pointers
        self.index = index
        self.coords = coords
        self.values = values
        # self.construct()

        self.intrapolate = True
        self.extrapolate = False


    def construct(self):

        pass

    def evaluate(self):

        pass


    def __call__(self,
                 coords: npt.ArrayLike):
        
        pass
