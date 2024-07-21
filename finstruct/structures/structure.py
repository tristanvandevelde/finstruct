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
                 dicttypes):
        
        """
        Data must be passed as dict somehow, to allow for:
        1. different types
        2. mapping to the space
        # """

        self._types = dicttypes
        self._data = {key: np.array(value, dtype=np.dtype(dicttypes[key])) for key, value in dictdata.items() if key in self._types.keys()}

    def __validate__(self):

        TYPECHECK(self._data, dict)
        for val in self._data.values():
            TYPECHECK(val, np.ndarray)

        ## Also make sure that every array has the same length.

    def select(self,
               index):
        
        cls = type(self)
        
        filtered_dict = {key: value[index] for key, value in self._data.items()}

        return cls(filtered_dict, self._types)
 
    def __len__(self):

        return np.array([len(arr) for arr in self._data.values()][0])
    
    def __getitem__(self,
                    items):
        
        """Gets only 1 item."""
        
        #items = np.asarray(items)
        #return [self._data[item] for item in items] # return list of np arrays
        key = np.asarray(items).flatten().item()

        return self._data[key]


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
                 dictdata,
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

        index_dictdata = {}
        for unitname in driver.Index.names:
            index_dictdata = {**index_dictdata, **{unitname: [row[unitname] for row in dictdata]}}

        coords_dictdata = {}
        for unitname in driver.Basis.names:
            coords_dictdata = {**coords_dictdata, **{unitname: [row[unitname] for row in dictdata]}}

        values_dictdata = {}
        for unitname in driver.Projection.names:
            values_dictdata = {**values_dictdata, **{unitname: [row[unitname] for row in dictdata]}}

        self._index = StructArray(index_dictdata, dict(zip(self._driver.Index.names, self._driver.Index.dtypes)))
        self._coords = StructArray(coords_dictdata, dict(zip(self._driver.Basis.names, self._driver.Basis.dtypes)))
        self._values = StructArray(values_dictdata, dict(zip(self._driver.Projection.names, self._driver.Projection.dtypes)))
        
        
    def __validate__(self):

        # TYPECHECK(self._driver, self._DRIVERTYPE)
        # LENCHECK(self._index, self._projection)
        # LENCHECK(self._basis, self._projection)


        pass

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
        
        return cls(data, driver, **kwargs)


    def _idx(self,
             **kwargs):
        
        """
        Given the conditions on each variable, return the index of the observations adhering to this.
        """

        index_conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Index.names}
        basis_conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Basis.names}

        index_idx = np.array([np.isin(self._index._data[str(variable)], condition) for variable, condition in index_conditions.items()])
        basis_idx = np.array([np.isin(self._coords._data[str(variable)], condition) for variable, condition in basis_conditions.items()])

        idx = np.array([all(tup) for tup in zip(*index_idx, *basis_idx)])

        return idx
    
    def _get(self,
             **kwargs):
        
        index_vals = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}
        index_grid = self._create_grid(*list(index_vals.values()))
        for index_combination in index_grid:
            self._interp()
        

    
    def _interpolate(self,
                     **kwargs):
        
        """
        
        """
        
        index_condition = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}
        values_condition = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        values_condition = StructArray(values_condition, dict(zip(self._driver.Basis.names, self._driver.Basis.dtypes)))

        idx = self._idx(**index_condition)
        coords_input = np.array(self._coords.select(idx)[self._driver.Basis.names], dtype=np.float64)
        values_input = np.array(self._values.select(idx)[self._driver.Projection.names], dtype=np.float64)
        coords_output = np.array(self._create_grid(values_condition[self._driver.Basis.names]), dtype=np.float64)

        cs = CubicSpline(coords_input.flatten(), values_input.flatten())
        values_output = cs(coords_output.flatten())

        return coords_output, values_output
    
    def get_values(self,
                   **kwargs):
        
        """
        In this function, all Basis variables are assumed to be given.
        """

        index_condition = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}
        coords_condition = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        index_grid = self._create_grid(*list(index_condition.values()))
        # filter out the ones that exist
        index_grid = [combination for combination in index_grid if dict(zip(self._driver.Index.names, combination)) in self._index]
        for index_value in index_grid:
            result = self._interpolate(**dict(zip(self._driver.Index.names, index_value)), **coords_condition)

        # if for the index variables no input is given, take all
        # if for the basis variables no input is given, the the defaults

        pass
        
        # kwargs = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        # if not Counter(list(kwargs.keys())) == Counter(self._driver.Basis.names):
        #     raise ValueError("All Basis variables need to be present.")
        #     # fill in with basis variables
        #     # missing_variables = [name for name in self._driver.Basis.names if name not in kwargs.keys()]
        #     # for var in missing_variables:
        #     #     kwargs[var] = np.unique(self._coords[var])

        # names = list(kwargs.keys())
        # values = list(kwargs.values())

        # grid = self._create_grid(*values)
        # results = np.empty(len(grid), dtype=dict)
        # for idx_outer, value in enumerate(grid):
        #     conditions = dict(zip(names, value))
        #     idx = self._idx(**conditions)
        #     if idx.any():
        #         val = self._vals.select(idx)
        #         results[idx_outer] = {**conditions, **val}
        #     else:
        #         val = self._interpolate(**dict(zip(names, value)))
        #         results[idx_outer] = {**conditions, **{"Rate": val}}

        # return results

    def _create_grid(self,
                    *args):
        
        """
        Each arg represents a variable for which we require the given values in a full grid.
        """

        grid = np.meshgrid(*args, indexing='ij')
        grid = np.array(grid).reshape(len(args),-1).T
        
        return grid

    
    def subset(self,
               **kwargs):

        
        return super().__init__(None)
    
    @classmethod
    def transform(cls,
                  object):
        
        TYPECHECK(object, super(cls))
       
        return cls.__init__(dictdata=object._dictdata, driver=object._driver)

    ## TODO:
    ## Implement filter or select, returning another Structure object.
    ## Subset.

    ## TODO:
    ## implement _dictdata