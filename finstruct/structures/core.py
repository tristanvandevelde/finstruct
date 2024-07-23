import csv
from collections import Counter

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.interpolate import interpn, RegularGridInterpolator, CubicSpline

from finstruct.utils.types import StructArray, Meta
from finstruct.utils.tools import create_grid
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver
from finstruct.interpolation.benchmark import Interpolation

# In __init__ of Structure:

        # create properties for unit values
        # for unit in self._driver:
        #     property()


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

        # compare with filter of StructArray

        index_conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Index.names}
        basis_conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Basis.names}

        index_idx = np.array([np.isin(self._index._data[str(variable)], condition) for variable, condition in index_conditions.items()])
        basis_idx = np.array([np.isin(self._coords._data[str(variable)], condition) for variable, condition in basis_conditions.items()])

        idx = np.array([all(tup) for tup in zip(*index_idx, *basis_idx)])

        return idx
    
    
    def _interpolate(self,
                     **kwargs):
        
        """
        All Basis variables are assumed to be given.
        """
        # check
        length = np.cumprod([len(list(options)) for options in list(kwargs.values())])[-1]

        # Should probably be replaced by StructArrays
        results = {
            "index": np.empty([length, self._driver.Index.size], dtype=self._driver.Index.dtypes[0]),
            "coords": np.empty((length, self._driver.Basis.size)),
            "values": np.empty((length, self._driver.Projection.size))
        }

        index_condition = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}        
        index_grid = create_grid(*list(index_condition.values()))

        values_condition = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        values_condition = StructArray(values_condition, dict(zip(self._driver.Basis.names, self._driver.Basis.dtypes)))

        coords_output = np.array(create_grid(values_condition[self._driver.Basis.names]), dtype=np.float64)

        """
        TODO: Preallocate. How to calculate grid size when both index & coords grid is being used?
        """

        for idx, combination in enumerate(index_grid):
            filter = dict(zip(self._driver.Index.names, combination))
            _idx = self._idx(**filter)

            coords_input = np.array(self._coords.select(_idx)[self._driver.Basis.names], dtype=np.float64)
            values_input = np.array(self._values.select(_idx)[self._driver.Projection.names], dtype=np.float64)

            cs = CubicSpline(coords_input.flatten(), values_input.flatten())
            values_output = cs(coords_output.flatten())

            #results.append([combination, coords_output, values_output])
            inner_grid_size = int(length/len(index_grid))
            slice_start = int(idx*inner_grid_size)

            results["index"][slice_start:slice_start+inner_grid_size] = combination
            results["coords"][slice_start:slice_start+inner_grid_size] = coords_output
            results["values"][slice_start:slice_start+inner_grid_size] = values_output[:,None]


        return results["index"], results["coords"], results["values"]


    def get_values(self,
                   **kwargs):
        
        """
        General function to extract values.
        If no condition is given for the index or basis, the default is assumed.
        Everything except this function is to be handled by the interpolation class.
        """

        index_condition = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}
        coords_condition = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}

        # if for the index variables no input is given, take all
        # if for the basis variables no input is given, the the defaults

        return self._interpolate(**index_condition, **coords_condition)
        

    def append(self,
               **kwargs):
        
        """Add observation to the structure.
        
        TODO: Check"""

        index_condition, coords_condition, values_condition = self._extract_conditions(kwargs)

        if not set(index_condition.keys()) == set(self._driver.Index.names):
            raise ValueError("Not all index variables are present")
        if not set(coords_condition.keys()) == set(self._driver.Basis.names):
            raise ValueError("Not all basis variables are present")
        if not set(values_condition.keys()) == set(self._driver.Projection.names):
            raise ValueError("Not all projection variables are present")
        
        if not all([len(val) for val in index_condition.values()] == 1):
            raise ValueError("Only one observation allowed")
        # do same for coords and values

        self._index.append(index_condition)
        self._coords.append(coords_condition)
        self._values.append(values_condition)


    def _extract_conditions(self,
                            conditions):
        
        index_condition = {key: value for key, value in conditions.items() if key in self._driver.Index.names}
        coords_condition = {key: value for key, value in conditions.items() if key in self._driver.Basis.names}
        values_condition = {key: value for key, value in conditions.items() if key in self._driver.Projection.names}

        return index_condition, coords_condition, values_condition


    @property
    def df(self):

        """TODO: Check"""

        # get values for all defaults
        index, coords, values = self.get_values()

        df = pd.DataFrame({**index._data, **coords._data, **values._data},
                          dtypes=[*index._dtypes, *coords._dtypes, *values._dtypes])
        
        return df
    

    def __add__(self,
                other):
        
        pass

    def __mul__(self,
                other):
        
        pass

    def __sub__(self,
                other):
        
        pass

    def convert(self,
                basis):
        
        """Convert the structure to a new Basis of the same kind.
        
        """
                          


    # def subset(self,
    #            **kwargs):
        
    #     return super().__init__(None)
    
    # @classmethod
    # def transform(cls,
    #               object):
    # Transform to different class
        
    #     TYPECHECK(object, super(cls))
       
    #     return cls.__init__(dictdata=object._dictdata, driver=object._driver)

