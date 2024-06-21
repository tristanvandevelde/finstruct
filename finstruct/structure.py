#import functools

from typing import Any
from collections import UserDict

import numpy as np
import numpy.typing as npt
from scipy.interpolate import RegularGridInterpolator

from finstruct.unit import Unit
from finstruct.basis import Basis
from finstruct.utils.checks import TYPECHECK



class Space:

    """
    The Space defines the dimensions and the units of structures.
    """

    def __init__(self,
                 coords: Basis,
                 vals: Basis):
        
        self.coords = coords
        self.vals = vals

        self.__validate__()

    def __validate__(self):

        """
        Assert that coords and vals are both arrays containing units.
        """

        TYPECHECK(self.coords, Basis)
        TYPECHECK(self.vals, Basis)




class Structure:

    """
    Structures are defined on spaces.
    """

    DEFAULTS = {
        "space": None #Basis(Unit())
    }

    def __init__(self,
                 data_coords,
                 data_vals,
                 space: Space,
                 name: str = None) -> None:
        

        self.name = name
        self.space = space
        
        self.coords = np.array(data_coords, dtype=self.basis.dtype_coords)
        self.values = np.array(data_vals, dtype=self.basis.dtype_vals)
        self.interpolation = RegularGridInterpolator

        self.interpolate = False

        self.__validate__()

    def __validate__(self):

        ## Set defaults if empty
        for attr in self.DEFAULTS:
            if self.attr is None:
                self.attr = self.DEFAULTS[attr]

        # if self.space is None:
        #     self.space = self.DEFAULTS["space"]

        ## Do checks

        #TYPECHECK(self.basis, Space)
        #SIZECHECK(self.coords, self.vals)

        # SIZECHECK dtypes & coords
        # SIZECHECK dtypes & vals

        if self.interpolation:
            """
            Perform interpolation on implied grid.
            """

    def idx(self,
            **kwargs):
        
        """
        Given the conditions on each variable, return the index for the observations adhering to this.
        """

        conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self.coords.dtype.names}
        idx = np.array([np.isin(self.coords[str(variable)], condition) for variable, condition in conditions.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        return idx


    def filter(self,
               **kwargs):
        
        """
        For given conditions on each variable, extract the observations adhering to these.
        """

        idx = self.idx(**kwargs)
        #return self.values[idx]
        result = self.values[idx]
        #return self.values.dtype
        # The issue with the folowwing is that a single Numpy Array can have only 1 type
        # return result.view(self.basis.dtype_vals.type).reshape(result.shape + (-1,))
        # Array
        #return result.view(np.float64).reshape(result.shape + (-1,))
        # Structured array
        return result.view().reshape(result.shape + (-1,))

    def create_grid(self,
                    *args):
        
    #     """
    #     Creates a grid of the requested values.
    #     """

        grid = np.meshgrid(*args, indexing='ij')
        grid = np.array(grid).reshape(len(args),-1).T
        
        return grid


    def get_values(self,
                   **kwargs):
        
        """
        Get values given by condition.
        """
        
        names = list(kwargs.keys())
        values = list(kwargs.values())

        grid = self.create_grid(*values)
        for value in grid.T:
            conditions = dict(zip(names, value))
            idx = self.filter(**conditions)
            if idx.any():
                val = self.values[idx]
            else:
                # interpolate
                pass

    def interpolate(self,
                    coords: npt.ArrayLike):
        
        coords_input = self.coords.view().reshape(self.coords.shape + (-1,))
        values_input = self.values.view().reshape(self.coords.shape + (-1,))


        interpolator = RegularGridInterpolator(coords_input, values_input, method="linear")

        return interpolator(coords)
    
    def _lincomb(self,
                 scalar,
                 other):
        pass
    
    # def __get__(self,
    #             **kwargs):
        

    #     ## TO IMPLEMENT
    #     pass

    # @property
    # def len(self):

    #     return len(self.vals)
    
    # @property
    # def ndim_coordinates(self):
    
    #     return self.coords.shape[0]
    
    # @property
    # def ndim_values(self):

    #     return self.vals.shape[0]
    