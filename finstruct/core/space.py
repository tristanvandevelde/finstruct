from itertools import chain, combinations

import numpy as np

from finstruct.utils.checks import TYPECHECK
from finstruct.utils.types import Meta
from finstruct.core.conventions import Convention
from finstruct.core.unit import Unit


## TODO: Check if the existence of Spaces is absolutely required here. 


class Space(metaclass=Meta):

    """A space is a collection of units that needs to be internally consistent.
    """

    def __init__(self,
                 *args):
        
        self.units = np.array(args)

    def __validate__(self):

        for unit in self.units:
            TYPECHECK(unit, Unit)

        for conv1, conv2 in combinations(self.conventions, 2):
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
    
    @property
    def dtypes(self):

        """
        Return the dtypes of the units.
        """

        return [unit.dtype for unit in self.units]

    @property
    def names(self):

        """
        Return the names of the units.
        """

        return [unit.name for unit in self.units]
    
    @property
    def size(self):

        return len(self.units)
    
    def __getitem__(self,
                    unitname):
        
        """
        Get the unit
        """
        
        return np.array([unit for unit in self.units if unit.name == unitname]).item()

    def __setitem__(self,
                    unitname,
                    unitval):
        
        "To implement"
        pass


    def convert(self,
                **kwargs):
        
        """Change a convention."""

        # Make sure kwargs holds each convention only once

        # Loop over all conventions that need to be changed
        for cname, convention in kwargs.items():
            #TYPECHECK(ctype, Convention)
            for idx, unit in enumerate(self.units):
                conv_names = [conv.__name__ for conv in unit.ctypes]
                if cname in conv_names:
                    unit.set_conventions(cname=convention)

        """
        TODO: Extend such that conversion functions are returned for each unit.
        """

    def CONVENTIONCHECK(self,
                        convention1,
                        convention2) -> None:
        
        if type(convention1) == type(convention2):
            if not convention1.value == convention2.value:
                raise ValueError(f"Conventions {convention1} and {convention2} do not match.")
            

