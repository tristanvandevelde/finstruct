import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from finstruct.utils.types import Meta
from finstruct.core.driver import VOLSurfaceDriver
from finstruct.structures.structure import Structure

class VOLSurface(Structure,
                 metaclass=Meta):

    _DRIVERTYPE = VOLSurfaceDriver

