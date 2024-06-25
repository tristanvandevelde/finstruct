from abc import ABCmeta

import numpy as np
import numpy.typing as npt

class Interpolation(metaclass=ABCmeta):

    def __init__(self,
                 coords: npt.ArrayLike,
                 values: npt.ArrayLike):
        
        self.coords = coords
        self.values = values
        self.construct()

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


