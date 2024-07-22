

#from abc import ABCmeta

import numpy as np
import numpy.typing as npt

from finstruct.structures.structure import StructArray
## TODO: move StructArray to tools

"""
Basic Python implementation of interpolation functionality.
Allows for the comparison and benchmarking of C++ implementation.
"""

class Interpolation(object):

    """Generic Interpolation class.

    Parameters
    ----------

    Method
    ------
    
    """

    def __init__(self,
                 coords: npt.ArrayLike,
                 values: npt.ArrayLike):
        
        # replace by pointers
        self.coords = coords
        self.values = values

        self.intrapolate = True
        self.extrapolate = False

    def construct(self):

        """
        Construct the required parameter values such that the evaluate function can be executed.
        """

    def evaluate(self,
                 **kwargs):
        
        # this function will call the construct function

        pass

    def prepare(self,
                **kwargs):
        
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
    



class Linear(Interpolation):

    pass

class CubicSpline(Interpolation):

    pass