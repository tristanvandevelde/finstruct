from itertools import chain

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
        
        self._data = {key: np.array(value, dtype=np.dtype(dicttypes[key])) for key, value in dictdata.items() if key in dicttypes.keys()}

    def idx(self,
            **kwargs):

        idx = np.array([np.isin(self._data[str(variable)], condition) for variable, condition in kwargs.items()])
        idx = np.array([all(tup) for tup in zip(*idx)])

        return idx


    def filter(self,
               **kwargs):
        
        cls = type(self)   

        index = self.idx(**kwargs)
        filtered_dict = {key: value[index] for key, value in self._data.items()}
        
        return cls(filtered_dict, dict(zip(self.names, self.dtypes)))


    def __getitem__(self,
                    item):
                
        keys = np.asarray(item)
        result = [self._data[key] for key in keys]
        if len(result) == 1:
            result = list(chain.from_iterable(result))

        return result

    def __setitem__(self,
                    item):
        
        raise NotImplementedError
    
    @property
    def values(self):

        return list(self._data.values())
    
    @property
    def names(self):

        return list(self._data.keys())
    
    @property
    def dtypes(self):

        return [arr.dtype for arr in self._data.values()]
    
    @property
    def dim(self):

        return len(self._data.keys()), np.array([len(arr) for arr in self._data.values()][0])

    # def append(self,
    #            **kwargs):
        
    #     """Add data point."""

    #     if not set(kwargs.keys()) == set(self._data.keys()):
    #         raise ValueError("Not all variables are present.")

    #     if not all([len(item) for item in list(kwargs.values())]) == 1:
    #         raise ValueError("Only one observation can be appended.")

    #     for key, value in kwargs.items():
    #         self._data[key] = np.append(self._data[key], value)

    # def __validate__(self):

    #     TYPECHECK(self._data, dict)
    #     for val in self._data.values():
    #         TYPECHECK(val, np.ndarray)

    #     ## Also make sure that every array has the same length.

    # def __iter__(self):

    #     pass

