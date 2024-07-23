import csv
from collections import Counter

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.interpolate import interpn, RegularGridInterpolator, CubicSpline

from finstruct.utils.types import Meta
from finstruct.utils.data import StructArray
from finstruct.utils.tools import create_grid
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver
from finstruct.interpolation.benchmark import Interpolation

# In __init__ of Structure:

        # create properties for unit values
        # for unit in self._driver:
        #     property()


"""TODO: How to implement a changing correlation structure over time?
Require an environment where the Basis has multiple units of the same type.

For example: 
    Index: Date
    Basis: [Price1, Price2, Price3]
    Projection: correlation

Interpolation should not be allowed there.
"""

class Structure(metaclass=Meta):

    """Structure class, holding data and methods related to a Driver.
    
    """

    def __init__(self,
                 name: str = None,
                 driver: Driver = None,
                 data: dict = None):
        
        _DEFAULTS = {
            "DRIVERTYPE": Driver
        }
        
        _DRIVERTYPE = Driver
        _DEFAULTDRIVER = Driver(None)
        # default should be taken from _DRIVERTYPE
        
        self.name = name
        self._driver = driver
        if data is not None:
            self.load(data)
        


    def load(self,
             dictdata):
        
        dicttypes = {
            **dict(zip(self._driver.Index.names, self._driver.Index.dtypes)),
            **dict(zip(self._driver.Basis.names, self._driver.Basis.dtypes)),
            **dict(zip(self._driver.Projection.names, self._driver.Projection.dtypes)),
        }

        dictdata_final = {}
        for unitname in list(dicttypes.keys()):
            dictdata_final = {**dictdata_final, **{unitname : [row[unitname] for row in dictdata]}}

        self.data = StructArray(dictdata_final, dicttypes)
        

    def __validate__(self):

        if self._driver is None:
            # take from drivertype
            self._driver = self._DEFAULTDRIVER
            #self._driver = Driver.read_config(f"config/drivers/{self._DEFAULTDRIVER}.ini")

        TYPECHECK(self._driver, self._DRIVERTYPE)



    @classmethod
    def read_csv(cls,
                 csvfile,
                 driver,
                 **kwargs):
        
        """
        Read from csvfile.
        """

        """Create Structure object from a .csv-file and Driver object.

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
        
        return cls(data=data, driver=driver, **kwargs)


    def __repr__(self):

        return f"{self.__class__.__name__}({self.name}, {repr(self._driver)})"
    

        


class Grid(Structure,
           metaclass=Meta):

    pass


class Manifold(Structure,
               metaclass=Meta):

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
                 name: str = None,
                 driver: Driver = None,
                 data: dict = None,
                 interpolator: object = None) -> None:
        
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

        super().__init__(name=name, driver=driver, data=data)
        self.interpolator = interpolator

        
    def __validate__(self):

        super().__validate__()
        if self.interpolator is None:
            self.interpolator = None
        # TYPECHECK(self.interpolator, None)

    
    
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

        index_condition, basis_condition, _ = self._extract_conditions(kwargs)

        index_grid = create_grid(*list(index_condition.values()))
        basis_grid = create_grid(*list(basis_condition.values()))

        for idx, combination in enumerate(index_grid):

            selection = dict(zip(self._driver.Index.names, combination))

            coords_input = np.array(self.data.filter(**selection)[self._driver.Basis.names], dtype=np.float64)
            values_input = np.array(self.data.filter(**selection)[self._driver.Projection.names], dtype=np.float64)

            cs = CubicSpline(coords_input.flatten(), values_input.flatten())
            values_output = cs(basis_grid.flatten())

            inner_grid_size = int(length/len(index_grid))
            slice_start = int(idx*inner_grid_size)

            results["index"][slice_start:slice_start+inner_grid_size] = combination
            results["coords"][slice_start:slice_start+inner_grid_size] = basis_grid
            results["values"][slice_start:slice_start+inner_grid_size] = values_output[:,None]

        return results["index"], results["coords"], results["values"]


    def get_values(self,
                   **kwargs):
        
        """
        General function to extract values.
        If no condition is given for the index or basis, the default is assumed.
        Everything except this function is to be handled by the interpolation class.
        """

        index_condition, basis_condition, _ = self._extract_conditions(kwargs)

        # if for the index variables no input is given, take all
        # if for the basis variables no input is given, the the defaults

        return self._interpolate(**index_condition, **basis_condition)
        

    # def append(self,
    #            **kwargs):
        
    #     """Add observation to the structure.
        
    #     TODO: Check"""

    #     index_condition, coords_condition, values_condition = self._extract_conditions(kwargs)

    #     if not set(index_condition.keys()) == set(self._driver.Index.names):
    #         raise ValueError("Not all index variables are present")
    #     if not set(coords_condition.keys()) == set(self._driver.Basis.names):
    #         raise ValueError("Not all basis variables are present")
    #     if not set(values_condition.keys()) == set(self._driver.Projection.names):
    #         raise ValueError("Not all projection variables are present")
        
    #     if not all([len(val) for val in index_condition.values()] == 1):
    #         raise ValueError("Only one observation allowed")
    #     # do same for coords and values

    #     self._index.append(index_condition)
    #     self._coords.append(coords_condition)
    #     self._values.append(values_condition)


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
    

    # def __add__(self,
    #             other):
        
    #     pass

    # def __mul__(self,
    #             other):
        
    #     pass

    # def __sub__(self,
    #             other):
        
    #     pass

    # def convert(self,
    #             basis):
        
    #     """Convert the structure to a new Basis of the same kind.
        
    #     """
                          


    # def subset(self,
    #            **kwargs):
        
    #     return super().__init__(None)
    
    # @classmethod
    # def transform(cls,
    #               object):
    # Transform to different class
        
    #     TYPECHECK(object, super(cls))
       
    #     return cls.__init__(name=object.name, dictdata=object._dictdata, driver=object._driver)

