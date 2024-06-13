import functools

import numpy as np

from finstruct.unit import Unit


"""
Space - Basis
Structure - Driver
"""

class Basis:

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
    def name_coords(self):

        return np.array([unit.name for unit in self.coords])

    @property
    def dtype_vals(self):
        
        return np.dtype([(self.vals.name, self.vals.dtype)])


class Driver:

    """
    Structures are defined on spaces.
    """

    DEFAULTS = {
        "BASIS": None #Basis(Unit())
    }

    def __init__(self,
                 data_coords,
                 data_vals,
                 basis: Basis,
                 name: str = None) -> None:
        

        self.name = name
        self.basis = basis
        
        self.coords = np.array(data_coords, dtype=self.basis.dtype_coords)
        self.values = np.array(data_vals, dtype=self.basis.dtype_vals)
        self.interpolation = None

        self.interpolation = False

        self.validate()

    def validate(self):

        ## Set defaults if empty
        if self.basis is None:
            self.basis = self.DEFAULTS["BASIS"]

        ## Do checks

        #TYPECHECK(self.basis, Space)
        #SIZECHECK(self.coords, self.vals)

        # SIZECHECK dtypes & coords
        # SIZECHECK dtypes & vals

        if self.interpolation:
            pass


    def fill(self):

        """
        Interpolate the driver on a discrete (full) grid.
        """


    def filter(self,
             **kwargs):
        
        """
        For given conditions on each variable, extract the observations adhering to these.
        """

        conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self.coords.dtype.names}
        idx = np.array([np.isin(self.coords[str(variable)], condition) for variable, condition in conditions.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        return idx

    

    # def get_grid(self,
    #              idx = None):

    #     """
    #     Creates a grid of the stored values.
    #     """

    #     if idx is None:
    #         idx = np.full(self.len, True)

    #     coords = self.coords[idx]
    #     uniquevals = [coords[name].unique() for name in self.coords.names]
        
    #     return self.create_grid(zip(self.coords.names, uniquevals))
        

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
        
        grid = self.create_grid(**kwargs)
        values = np.empty((len(grid), self.ndim_values))

        for idx, coordinates in grid:
            try:
                _, _, values[idx] = self.filter(zip(self.coords.names, coordinates))
            except:
                ## interpolate
                pass

        return values

    
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
    

    ## Combining structures can also be generally implemented



