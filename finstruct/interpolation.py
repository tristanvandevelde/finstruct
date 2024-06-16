import numpy as np
import numpy.typing as npt

class Interpolation:

    def __init__(self,
                 coords: npt.ArrayLike,
                 values: npt.ArrayLike):
        
        self.coords = coords
        self.values = values

        self.intrapolate = True
        self.extrapolate = False

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
        it = np.nditer(values, flas=["f_index"])
        for _ in it:
            values[it.index] = self.evaluate(coords[it.index])
        
        return values
            