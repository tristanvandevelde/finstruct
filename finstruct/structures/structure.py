import numpy as np
import numpy.typing as npt
from scipy.interpolate import RegularGridInterpolator


from finstruct.utils.types import Meta
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver

# Add Structure metaclass to create properties for all variables.

# Issue here can arise when a certain unit is present more than once
# class AxisGetter(object):
#     def __init__(self, name):
#         self.name = name

#     def __call__(self, owner):
#         units = getattr(owner, "_DIMENSIONS")
#         return units[self.name]
    
# class AxisSetter(object):
#     def __init__(self, name):
#         self.name = name

#     def __call__(self, owner, value):
#         units = getattr(owner, "_DIMENSIONS")
#         units[self.name] = Space(*value) #value
#         return setattr(owner, "_DIMENSIONS", units)

# In __init__ of Structure:

        # create properties for unit values
        # for unit in self._driver:
        #     property()

## TODO: Merge with utils.types.FLDict
class StructArray(object,
                  metaclass=Meta):

    """Alternative to numpy structured arrays.

    """

    def __init__(self,
                 dictdata,
                 space):
        
        """
        Data must be passed as dict somehow, to allow for:
        1. different types
        2. mapping to the space
        # """

        self._data = {key: np.array(value, dtype=np.dtype(space[key].dtype)) for key, value in dictdata.items()}

    def __validate__(self):

        TYPECHECK(self._data, dict)
        for val in self._data.values():
            TYPECHECK(val, np.ndarray)

        ## Also make sure that every array has the same length.

    def __getitem__(self,
                    idx):
        """
        Return the observations adhering to this stuff.
        """
        
        return {key: value[idx] for key, value in self._data.items()}
    
    def __getslice__(self):

        """
        Return all data when using the slice.
        """

        return self._data

    def __setitem__(self,
                    *args):
        
        raise NotImplementedError
    
    @property
    def len(self):

        return np.array([len(arr) for arr in self._data.values()]).item()

class Structure(metaclass=Meta):

    """Structure class.
    
    Attributes
    ----------
    name: str
        Name of the structure
    driver: Driver
        Driver of the structure
    
    """

    _DRIVERTYPE = Driver
    # _DEFAULTDRIVER = None
    _DEFAULTDRIVER = "StructureDefault"
    _DEFAULTINTERPOLATION = RegularGridInterpolator

    def __init__(self,
                 coords_dictdata: dict,
                 values_dictdata: dict,
                 driver: Driver,
                 name = None,
                 interpolator = None) -> None:
        
        ## TODO:
        # Maybe should change to dicts of 1D numpy arrays

        #self._coords = dict(zip(driver.Basis.names), np.array())
        
        """
        Initialize Structure.

        Parameters
        ----------
        data_coords: list[C,N]
            Coordinates of the data to load in.
        data_vals: list[1,N]
            Values of the data to load in.
        driver: Driver
            Driver to use for construction.
        name: str
            Name of the Structure to be set.
        """

        self.name = name
        
        if driver is None:
            self._driver = Driver.read_config(f"config/drivers/{self._DEFAULTDRIVER}.ini")
        else:
            self._driver = driver

        self._coords = StructArray(coords_dictdata, self._driver.Basis)
        self._vals = StructArray(values_dictdata, self._driver.Projection)

        # self._coords = np.core.records.fromarrays(np.asarray(data_coords).transpose(),
        #                                           names = self._driver.Basis.names,
        #                                           formats = self._driver.Basis.dtypes)
        
        # self._vals = np.core.records.fromarrays(np.asarray(data_vals).transpose(),
        #                                         names = self._driver.Projection.names,
        #                                         formats = self._driver.Projection.dtypes)
        
        if interpolator is None:
            interpolator = self._DEFAULTINTERPOLATION
        self.interpolation = interpolator

        self._set_interpolators()

        
    def __validate__(self):

        TYPECHECK(self._driver, self._DRIVERTYPE)
        # LENCHECK(self._coords, self._vals)

    def __repr__(self):

        return f"{self.__class__.__name__}({self.name}, {repr(self._driver)})"
    
    @property
    def coords(self):
        pass

    def vals(self):
        pass

    @classmethod
    def read_csv(self,
                 csvfile):
        
        """
        Read from csvfile.
        """

    def _set_interpolators(self) -> None:
        
        args = [unitname for unitname, dtype in zip(self._driver.Basis.names, self._driver.Basis.dtypes) if np.dtype(dtype) == "d"]

        # else:
        #     args = [unitname for unitname in args if unitname in self._driver.Basis.names]

        self.__interpolate__ = args

    # @property
    # def ndim(self):

    #     ndim = {
    #         "Basis": self._coords.shape,
    #         "Projection": self._values.shape
    #     }

    #     return ndim
    
    # def __get__(self,
    #             **kwargs):
        
    #     # fill in with basis variables
    #     kwargs = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
    #     missing_variables = [name for name in self._driver.Basis.names if name not in kwargs.keys()]
    #     for var in missing_variables:
    #         kwargs[var] = np.unique(self._coords[var])

    #     return self.get_values(**kwargs)

    def idx(self,
            **kwargs):
        
        """
        Given the conditions on each variable, return the index of the observations adhering to this.
        """

        conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Basis.names}


        idx = np.array([np.isin(self._coords[:][str(variable)], condition) for variable, condition in conditions.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        print(idx)

    #     return idx

    # def filter(self,
    #            idx):
        
    #     """
    #     For given conditions on each variable, extract the observations adhering to these.
    #     """

    #     coords = self._coords[idx].copy()
    #     coords = coords.view(type=np.matrix).reshape(coords.shape + (-1,))

    #     vals = self._vals[idx].copy()
    #     vals = vals.view(type=np.matrix, dtype=np.float64).reshape(vals.shape + (-1,))

    #     return coords, vals
    
    def format(self,
               *args):
        
        pass
    
    # def _interpolate(self,
    #                  coords: npt.ArrayLike):
        
    #     """
    #     Should take in an array with values of all the units in the basis.
    #     """

    #     # First, we need to group by values of non-interpolating variables.
    #     # These will create the input data for the interpolator
    #     # Then construct the interpolator
    #     # Then interpolate the other variables.
    #     # This will be rather loopy, so might need to move to C++.
    #     length = np.asarray(coords.shape).item()
    #     dimension = self._driver.Projection.size
    #     if dimension != 1:
    #         raise NotImplementedError("Multivariate interpolation not supported")

    #     result = np.empty((length, dimension))

    #     index_vars = [var for var in self._driver.Basis.names if var not in self.__interpolate__]

    #     unique_index_vars = np.unique(coords[index_vars])

    #     for combination in unique_index_vars:

    #         idx = (self._coords[index_vars] == combination)
    #         if idx.sum() == 0:
    #             raise ValueError("Can't interpolate on index variables.")
            
    #         coords_input = np.array(self._coords[idx][self.__interpolate__].copy(), dtype=np.float64)
    #         coords_input = coords_input.reshape(coords_input.shape + (-1,))

    #         # For multivariate interpolation, here we still need to loop over the values.
    #         values_input = np.array(self._vals[idx]["Rate"].copy(), dtype=np.float64)
    #         values_input = values_input.reshape(values_input.shape + (-1,))

    #         interpolator = RegularGridInterpolator(coords_input.T, values_input, method="linear")

    #         coords_output = np.array(coords[idx][self.__interpolate__], dtype=np.float64)
    #         coords_output = coords_output.reshape(coords_output.shape + (-1,))

    #         result[idx] = interpolator(coords_output)

    #     return result
    
    # def get_values(self,
    #                **kwargs):
        
    #     """
    #     In this function, all Basis variables are assumed to be given.
    #     """
        
    #     kwargs = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
    #     if not list(kwargs.keys()) == self._driver.Basis.names:
    #         raise ValueError("All Basis variables need to be present.")

    #     names = list(kwargs.keys())
    #     values = list(kwargs.values())

    #     grid = self.create_grid(*values)
    #     print(grid)
    #     for value in grid:
    #         conditions = dict(zip(names, value))
    #         idx = self.idx(**conditions)
    #         if idx.any():
    #             _, val = self.filter(idx)
    #             print(val)
    #         else:
    #             print("Require interpolation")


    # def create_grid(self,
    #                 *args):
        
    #     """
    #     Each arg represents a variable for which we require the given values in a full grid.
    #     """

    #     grid = np.meshgrid(*args, indexing='ij')
    #     grid = np.array(grid).reshape(len(args),-1).T
        
    #     return grid

    
