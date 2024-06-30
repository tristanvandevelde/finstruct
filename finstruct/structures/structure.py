import csv
from collections import Counter

import numpy as np
import numpy.typing as npt
from scipy.interpolate import interpn, RegularGridInterpolator, CubicSpline

from finstruct.utils.types import Meta
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver

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


    def select(self,
               index):
        
        return {key: value[index] for key, value in self._data.items()}
 
    def __len__(self):

        return np.array([len(arr) for arr in self._data.values()][0])

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
    _DEFAULTDRIVER = "StructureDefault"
    _DEFAULTINTERPOLATION = RegularGridInterpolator

    def __init__(self,
                 coords_dictdata: dict,
                 values_dictdata: dict,
                 driver: Driver,
                 name = None,
                 interpolator = None) -> None:
        
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
        
        if interpolator is None:
            interpolator = self._DEFAULTINTERPOLATION
        self.interpolation = interpolator

        self._set_interpolators()

        
    def __validate__(self):

        TYPECHECK(self._driver, self._DRIVERTYPE)
        LENCHECK(self._coords, self._vals)

    def __repr__(self):

        return f"{self.__class__.__name__}({self.name}, {repr(self._driver)})"

    @classmethod
    def read_csv(cls,
                 csvfile,
                 driver,
                 **kwargs):
        
        """
        Read from csvfile.
        """

        """Create Structure object from a .csv-file and driver object (can later be config file).

        Parameters
        ----------
        csvfile: str
            Location of the .csv-file.
        driver: Driver
            Driver to drive the structure.

        Notes
        -----
        The .csv-file is expected to have as headers all the units present in the Driver.
        """
        
        with open(file=csvfile, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)
        
        coords = {}
        for unitname in driver.Basis.names:
            coords = {**coords, **{unitname: [row[unitname] for row in data]}}

        values = {}
        for unitname in driver.Projection.names:
            values = {**values, **{unitname: [row[unitname] for row in data]}}

        return cls(coords, values, driver, **kwargs)



    def _set_interpolators(self) -> None:
        
        args = [unitname for unitname, dtype in zip(self._driver.Basis.names, self._driver.Basis.dtypes) if np.dtype(dtype) == "d"]

        # else:
        #     args = [unitname for unitname in args if unitname in self._driver.Basis.names]

        self.__interpolate__ = args

    def _idx(self,
             **kwargs):
        
        """
        Given the conditions on each variable, return the index of the observations adhering to this.
        """

        conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Basis.names}


        idx = np.array([np.isin(self._coords._data[str(variable)], condition) for variable, condition in conditions.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        return idx

    
    def _interpolate(self,
                     **kwargs):
        
        """
        Should take in a dict with values of all the units in the basis.
        """

        index_vars = [var for var in self._driver.Basis.names if var not in self.__interpolate__]
        unique_index_vals = np.unique([value for key, value in kwargs.items() if key in index_vars])

        # Somehow check that this is 1 dimensional
        idx = self._idx(**dict(zip(index_vars, unique_index_vals)))
        if idx.sum() == 0:
            raise ValueError("Can't interpolate on index variables.")
        
        coords_input = {key: value for key, value in self._coords.select(idx).items() if key in self.__interpolate__}
        coords_input = np.array(list(coords_input.values()), dtype=np.float64).T
        
        values_input = np.array(list(self._vals.select(idx).values()), dtype=np.float64).T

        # really improve this stuff
        coords_output = {key: value for key, value in kwargs.items() if key in self.__interpolate__}
        coords_output = np.array(list(coords_output.values()), dtype=np.float64).T

        cs = CubicSpline(coords_input.T.flatten(), values_input.T.flatten())

        result = cs(coords_output.T.flatten(), 2)

        return result

    
    def get_values(self,
                   **kwargs):
        
        """
        In this function, all Basis variables are assumed to be given.
        """
        
        kwargs = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        if not Counter(list(kwargs.keys())) == Counter(self._driver.Basis.names):
            raise ValueError("All Basis variables need to be present.")
            # fill in with basis variables
            # missing_variables = [name for name in self._driver.Basis.names if name not in kwargs.keys()]
            # for var in missing_variables:
            #     kwargs[var] = np.unique(self._coords[var])

        names = list(kwargs.keys())
        values = list(kwargs.values())

        grid = self._create_grid(*values)
        results = np.empty(len(grid), dtype=dict)
        for idx_outer, value in enumerate(grid):
            conditions = dict(zip(names, value))
            idx = self._idx(**conditions)
            if idx.any():
                val = self._vals.select(idx)
                results[idx_outer] = {**conditions, **val}
            else:
                val = self._interpolate(**dict(zip(names, value)))
                results[idx_outer] = {**conditions, **{"Rate": val}}

        return results

    def _create_grid(self,
                    *args):
        
        """
        Each arg represents a variable for which we require the given values in a full grid.
        """

        grid = np.meshgrid(*args, indexing='ij')
        grid = np.array(grid).reshape(len(args),-1).T
        
        return grid

    
