from typing import Any

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.tools import Meta
#from finstruct.driver import Driver
from finstruct.unit import Unit


class Basis:

    """
    Class to hold connection between drivers.
    """

    def __init__(self,
                 *args) -> None:
        
        self.drivers = args

        self.__validate__()

    def __validate__(self):

        for driver in self.drivers: TYPECHECK(driver, Unit)

        return True

    def __repr__(self):
        
        return "Basis({})".format(*[repr(driver) for driver in self.drivers])
    
    @property
    def dtypes(self):

        return np.dtype([(unit.name, unit.dtype) for unit in self.drivers])
    
    @property
    def names(self):

        return np.array([unit.name for unit in self.drivers])




