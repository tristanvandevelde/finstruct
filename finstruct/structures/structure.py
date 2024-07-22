import csv
from collections import Counter

import numpy as np
import numpy.typing as npt
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

        index_condition = {key: value for key, value in kwargs.items() if key in self._driver.Index.names}        
        index_grid = create_grid(*list(index_condition.values()))

        values_condition = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}
        values_condition = StructArray(values_condition, dict(zip(self._driver.Basis.names, self._driver.Basis.dtypes)))

        results = []

        for combination in index_grid:
            filter = dict(zip(self._driver.Index.names, combination))
            idx = self._idx(**filter)

            coords_input = np.array(self._coords.select(idx)[self._driver.Basis.names], dtype=np.float64)
            values_input = np.array(self._values.select(idx)[self._driver.Projection.names], dtype=np.float64)
            coords_output = np.array(create_grid(values_condition[self._driver.Basis.names]), dtype=np.float64)

            cs = CubicSpline(coords_input.flatten(), values_input.flatten())
            values_output = cs(coords_output.flatten())

            results.append([combination, coords_output, values_output])

        return results


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
        




    
    # def subset(self,
    #            **kwargs):

        
    #     return super().__init__(None)
    
    # @classmethod
    # def transform(cls,
    #               object):
        
    #     TYPECHECK(object, super(cls))
       
    #     return cls.__init__(dictdata=object._dictdata, driver=object._driver)

