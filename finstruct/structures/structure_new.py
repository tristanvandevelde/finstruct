import numpy as np
from scipy.interpolate import RegularGridInterpolator


from finstruct.utils.types import Meta
from finstruct.utils.checks import TYPECHECK, LENCHECK
from finstruct.core.driver import Driver

class Structure(metaclass=Meta):

    _DRIVERTYPE = Driver

    def __init__(self,
                 data_coords,
                 data_vals,
                 driver: Driver,
                 name = None) -> None:

        self.name = name
        self._driver = driver
        self.interpolation = RegularGridInterpolator

        self._coords = np.core.records.fromarrays(np.asarray(data_coords).transpose(),
                                                  names = self._driver.Basis.names,
                                                  formats = self._driver.Basis.dtypes)
        
        self._vals = np.core.records.fromarrays(np.asarray(data_vals).transpose(),
                                                names = self._driver.Projection.names,
                                                formats = self._driver.Projection.dtypes)

        

    def __validate__(self):

        TYPECHECK(self._driver, self._DRIVERTYPE)
        LENCHECK(self._coords, self._vals)

