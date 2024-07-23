import numpy as np

from finstruct.utils.types import Meta
from finstruct.utils.checks import TYPECHECK


class StructArray(object,
                  metaclass=Meta):

    """Alternative to numpy structured arrays.

    """

    def __init__(self,
                 dictdata,
                 dicttypes):
        
        self._types = dicttypes
        self._data = {key: np.array(value, dtype=np.dtype(dicttypes[key])) for key, value in dictdata.items() if key in self._types.keys()}

        # Make Fixed such that no new variables can be added after initialization.

    def __validate__(self):

        TYPECHECK(self._data, dict)
        for val in self._data.values():
            TYPECHECK(val, np.ndarray)

        ## Also make sure that every array has the same length.

    def select(self,
               index):
        
        cls = type(self)
        
        filtered_dict = {key: value[index] for key, value in self._data.items()}

        return cls(filtered_dict, self._types)
 

    def idx(self,
            **kwargs):

        idx = np.array([np.isin(self._data[str(variable)], condition) for variable, condition in kwargs.items()])
        return idx


    def filter(self,
               **kwargs):
        
        cls = type(self)    
        index = self.idx(**kwargs)
        filtered_dict = {key: value[index] for key, value in self._data.items()}
        return cls(filtered_dict, self._types)

    def __len__(self):

        return np.array([len(arr) for arr in self._data.values()][0])
    
    def __getitem__(self,
                    item):
                
        key = np.asarray(item).flatten().item()

        return self._data[key]
    
    def __setitem__(self,
                    item):
        
        raise NotImplementedError
    
    def values(self):

        return self._data.values()
    
    @property
    def names(self):

        return list(self._data.keys())
    
    def __iter__(self):

        pass
    
    def filter(self,
               **kwargs):
        
        basis_idx = np.array([np.isin(self._data[str(variable)], condition) for variable, condition in kwargs.items()])

        #print(basis_idx)
        #idx = np.array([all(tup) for tup in basis_idx])

        return basis_idx
    
    def append(self,
               **kwargs):
        
        """Add data point."""

        if not set(kwargs.keys()) == set(self._data.keys()):
            raise ValueError("Not all variables are present.")

        if not all([len(item) for item in list(kwargs.values())]) == 1:
            raise ValueError("Only one observation can be appended.")

        for key, value in kwargs.items():
            self._data[key] = np.append(self._data[key], value)