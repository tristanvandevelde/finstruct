
from typing import Any
from collections import UserDict

from finstruct.unit import Unit, TermUnit, DateUnit, DaycountUnit
from finstruct.utils.checks import TYPECHECK

class Driver:

    """
    An axis, dimension or driver (final name to be decided) is a wrapper around a unit.

    """

    utype = Unit
    DEFAULTS = {
        "convention": None
    }

    def __init__(self,
                 convention: str = None,
                 **kwargs) -> None:
        
        """
        Load in, and assert that all values are drivers.
        """
        
        #self.unit = self.utype(convention)
        self.unit = convention
        self.interpolation = False      # information about interpolation method
        self.defaults = None            # default values

    @property
    def name(self):

        return self.unit.name
    
    def __repr__(self) -> str:
        
        return f"{type(self).__name__}(test)"



class TimeDriver(Driver):

    utype = [TermUnit, DateUnit]

    def __init__(self,
                 unit,
                 dc_unit,
                 **kwargs):
        
        TYPECHECK(dc_unit, DaycountUnit)

        super().__init__(unit=unit, dc_unit=dc_unit)

class TermAxis(TimeDriver):

    utype = TermUnit

class DateAxis(TimeDriver):

    utype = DateUnit
