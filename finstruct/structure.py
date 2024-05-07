import functools

import numpy as np

from finstruct.unit import Unit
from finstruct.basis import Space
from finstruct.tools import TYPECHECK, SIZECHECK, DIMCHECK

class Structure:

    """
    Structures are defined on spaces.
    """

    def __init__(self,
                 data_coords,
                 data_vals,
                 space: Space = None,
                 interpolation = None) -> None:
        
        self.basis = space

        self.dtype_coords = np.dtype([(unit.name, unit.dtype) for unit in self.basis.coords])
        self.dtype_vals = np.dtype([(self.basis.vals.name, self.basis.vals.dtype)])

        self.coords = np.array(data_coords, dtype=self.dtype_coords)
        self.vals = np.array(data_vals, dtype=self.dtype_vals)

        self.interpolate = None

        #self.validate()

    def validate(self):

        ## Set defaults if empty
        if space is None:
            space = self.DEFAULTS["BASIS"]

        ## Do checks

        TYPECHECK(self.basis, Space)

        SIZECHECK(self.coords, self.vals)

        # SIZECHECK dtypes & coords
        # SIZECHECK dtypes & vals
        DIMCHECK("test", "test")

        ## Idea: if checks fail, replace by default

    @property
    def data(self):
        
        return np.array([self.coords, self.vals])
    
    def filter(self,
               **kwargs):
        


        conditions = [np.isin(self.coords[str(key)], np.array(value).flatten()) for key, value in kwargs.items()]
        idx = functools.reduce(lambda a, b: a & b, conditions)

        return idx, self.coords[idx], self.vals[idx]
    

    
    def get_grid(self,
                 idx = None):

        """
        Creates a grid of the stored values.
        """

        if idx is None:

            idx = np.full(self.len, True)

        coords = self.coords[idx]


        uniquevals = [coords[name].unique() for name in self.coords.names]
        
        return self.create_grid(zip(self.coords.names, uniquevals))
        

    def create_grid(self,
                    **kwargs):
        
        """
        Creates a grid of the requested values.
        """

        uniquevals = np.array(kwargs.values())

        grid = np.array(np.meshgrid(*uniquevals, indexing='ij'))
        grid = grid.reshape(3,-1).T

        return grid

    
    def __get__(self,
                **kwargs):
        

        grid = self.create_grid(**kwargs)
        values = np.empty((len(grid), self.ndim_values))

        for idx, coordinates in grid:
            try:
                _, _, values[idx] = self.filter(zip(self.coords.names, coordinates))
            except:
                ## interpolate
                pass



    @property
    def len(self):

        return len(self.vals)
    
    @property
    def ndim_coordinates(self):
    
        return self.coords.shape[0]
    
    @property
    def ndim_values(self):

        return self.vals.shape[0]
    

    ## Combining structures can also be generally implemented



