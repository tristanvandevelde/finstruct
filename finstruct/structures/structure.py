import numpy as np
import numpy.typing as npt
from scipy.interpolate import RegularGridInterpolator


from finstruct.utils.types import Meta
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver

# Add Structure metaclass to create properties for all variables.

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

    def __init__(self,
                 data_coords,
                 data_vals,
                 driver: Driver,
                 name = None) -> None:
        
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
        self._driver = driver

        self._coords = np.core.records.fromarrays(np.asarray(data_coords).transpose(),
                                                  names = self._driver.Basis.names,
                                                  formats = self._driver.Basis.dtypes)
        
        self._vals = np.core.records.fromarrays(np.asarray(data_vals).transpose(),
                                                names = self._driver.Projection.names,
                                                formats = self._driver.Projection.dtypes)
        
        # create properties for unit values
        # for unit in self._driver:
        #     property()

        self.interpolation = RegularGridInterpolator
        self.__interpolate__ = [] # list of coordinate units to allow interpolation over.
        # As standard, set all numeric units in the basis driver.

        
    def __validate__(self):

        TYPECHECK(self._driver, self._DRIVERTYPE)
        LENCHECK(self._coords, self._vals)

    def set_interpolators(self,
                            *args):
        
        args = [unitname for unitname in args if unitname in self._driver.Basis.names]

        self.__interpolate__ = args

    @property
    def ndim(self):

        ndim = {
            "Basis": self._coords.shape,
            "Projection": self._values.shape
        }

        return ndim
    
    def __get__(self,
                **kwargs):
        pass

    def idx(self,
            **kwargs):
        
        """
        Given the conditions on each variable, return the index of the observations adhering to this.
        """

        conditions = {variable: np.asarray(condition) for variable, condition in kwargs.items() if variable in self._driver.Basis.names}
        idx = np.array([np.isin(self._coords[str(variable)], condition) for variable, condition in conditions.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        return idx

    def filter(self,
               idx):
        
        """
        For given conditions on each variable, extract the observations adhering to these.
        """

        coords = self._coords[idx].copy()
        coords = coords.view(type=np.matrix).reshape(coords.shape + (-1,))

        vals = self._vals[idx].copy()
        vals = vals.view(type=np.matrix, dtype=np.float64).reshape(vals.shape + (-1,))

        return coords, vals
    
    def format(self,
               *args):
        
        pass
    
    def interpolate(self,
                    coords: npt.ArrayLike):
        
        coords_input = np.array(self._coords[self.__interpolate__].copy(), dtype=np.float64)
        coords_input = coords_input.reshape(coords_input.shape + (-1,))

        values_input = np.array(self._vals["Rate"].copy(), dtype=np.float64)
        values_input = values_input.reshape(values_input.shape + (-1,))

        interpolator = RegularGridInterpolator(coords_input.T, values_input, method="linear")


        return interpolator(coords)
    
    def get_values(self,
                   **kwargs):
        
        """
        How to solve: ideally, all Basis variables should be provided.
        """
        
        kwargs = {key: value for key, value in kwargs.items() if key in self._driver.Basis.names}

        # TODO: How so solve for variables that have not been given?

        names = list(kwargs.keys())
        values = list(kwargs.values())

        grid = self.create_grid(*values)
        print(grid)
        for value in grid:
            conditions = dict(zip(names, value))
            idx = self.idx(**conditions)
            if idx.any():
                _, val = self.filter(idx)
                print(val)
            else:
                print("Require interpolation")


    def create_grid(self,
                    *args):
        
        """
        Each arg represents a variable for which we require the given values in a full grid.
        """

        grid = np.meshgrid(*args, indexing='ij')
        grid = np.array(grid).reshape(len(args),-1).T
        
        return grid

    
