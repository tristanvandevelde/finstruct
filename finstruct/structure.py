import functools

import numpy as np



"""
Space - Basis
Structure - Driver
"""


class Space:

    """
    The Space defines the dimensions and the units of structures.
    """

    def __init__(self,
                 coords,
                 vals):
        
        self.coords = coords
        self.vals = vals

        self.validate()

    def validate(self):

        """
        Assert that coords and vals are both arrays containing units.
        """

    @property
    def dtype_coords(self):

        return np.dtype([(unit.name, unit.dtype) for unit in self.coords])

    @property
    def dtype_vals(self):
        
        return np.dtype([(self.vals.name, self.vals.dtype)])

class Structure:

    """
    Structures are defined on spaces.
    """

    def __init__(self,
                 data_coords,
                 data_vals,
                 space: Space,
                 name: str = None) -> None:
        

        self.name = name
        self.basis = space

        self.coords = np.array(data_coords, dtype=self.basis.dtype_coords)
        self.values = np.array(data_vals, dtype=self.basis.dtype_vals)

        self.interpolation = None


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

        ## Perform interpolation if necessary
        if self.interpolation:

            grid = self.get_grid()
            # create values
            # fill in known values
            # interpolate unknown values
            # set coo and values


    
    def filter(self,
               **kwargs):
        


        conditions = [np.isin(self.coords[str(key)], np.array(value).flatten()) for key, value in kwargs.items()]
        idx = functools.reduce(lambda a, b: a & b, conditions)

        return idx, self.coords[idx], self.values[idx]
    

    
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
        grid = grid.reshape(self.ndim_coordinates,-1).T

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

        return values

    def select(self):
        pass

    def get_values(self):
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



