from itertools import chain, combinations

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.types import Meta
from finstruct.core.conventions import Convention
from finstruct.core.unit import Unit



class Space(metaclass=Meta):

    """A space is a collection of units that needs to be internally consistent.
    """

    def __init__(self,
                 *args):
        
        self.units = np.array(args)

    def __validate__(self):

        for unit in self.units:
            TYPECHECK(unit, Unit)

        for conv1, conv2 in combinations(self.conventions):
            self.CONVENTIONCHECK(conv1, conv2)

    def __repr__(self):

        return f"Space{(tuple([repr(unit) for unit in self.units]))}".replace("\"","")

    @property
    def conventions(self):

        conventions = [list(unit.conventions.values()) for unit in self.units]

        return list(chain.from_iterable(conventions))

    @property
    def ctypes(self):

        ctypes = [unit.ctypes for unit in self.units]

        return set(chain.from_iterable(ctypes))

    def convert(self,
                **kwargs):
        
        """Change a convention."""

        for ctype, convention in kwargs:
            #TYPECHECK(ctype, Convention)
            for idx, unit in enumerate(self.units):
                if ctype in [ctype.name for ctype in unit.ctypes]:
                    self.units[idx] = unit.convert(ctype=convention)

    def CONVENTIONCHECK(self,
                        convention1,
                        convention2) -> None:
        
        if type(convention1) == type(convention2):
            if not convention1.value == convention2.value:
                raise ValueError(f"Conventions {convention1} and {convention2} do not match.")
            

    def get_units(self,
                  convention) -> list:
        
        """Return units that contain the convention"""

        return [unit for unit in self.units if type(unit.convention) == type(convention)]


