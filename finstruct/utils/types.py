from collections.abc import MutableMapping
## TODO: Merge with utils.types.FLDict
#
# Alternative to compound np array for easier handling


from finstruct.utils.checks import TYPECHECK

import numpy as np


class FLDict(MutableMapping):

    """
    Dict-like object with fixed keys and lists as values.
    """
    
    def __init__(self, *args, **kwargs):
        
        
        self._dictionary = {**{name: [] for name in args}, 
                            **{key: list(value) for key, value in kwargs.items()}}
        
    def __setitem__(self, key, item):
        if key not in self._dictionary:
            raise KeyError("The key {} is not defined.".format(key))
        self._dictionary[key] = item
        
    def __getitem__(self, key):
        return self._dictionary[key]
    
    def __iter__(self):
        return iter(self._dictionary)

    def __len__(self):
        return len(self._dictionary)
    
    def __delitem__(self):
        raise NotImplementedError
        
    def __repr__(self):
        
        return f"{self.__class__.__name__}({self._dictionary})"
    
    def __str__(self):
        
        return str(self._dictionary)

class Meta(type):

    """
    Adds the __validate__ method to each class, and executes it after the initialization.
    """

    ## TODO: Extend with **kwargs such that DriverMeta can inherit from it.
    # https://stackoverflow.com/questions/13762231/how-to-pass-arguments-to-the-metaclass-from-the-class-definition
    # 
    
    @classmethod
    def __prepare__(mcs, name, bases):

        namespace = {
            **super().__prepare__(mcs, name, bases),
            "__validate__": lambda *args: None
        }

        return namespace
         
    def __call__(cls, *args, **kwargs):

        #obj = super(Meta, cls).__call__(*args, **kwargs)
        obj = super().__call__(*args, **kwargs)
        obj.__validate__()

        return obj


class FLDict(MutableMapping):

    """
    Dict-like object with fixed keys and lists as values.
    """
    
    def __init__(self, *args, **kwargs):
        
        
        self._dictionary = {**{name: [] for name in args}, 
                            **{key: list(value) for key, value in kwargs.items()}}
        
    def __setitem__(self, key, item):
        if key not in self._dictionary:
            raise KeyError("The key {} is not defined.".format(key))
        self._dictionary[key] = item
        
    def __getitem__(self, key):
        return self._dictionary[key]
    
    def __iter__(self):
        return iter(self._dictionary)

    def __len__(self):
        return len(self._dictionary)
    
    def __delitem__(self):
        raise NotImplementedError
        
    def __repr__(self):
        
        return f"{self.__class__.__name__}({self._dictionary})"
    
    def __str__(self):
        
        return str(self._dictionary)


class StructArray(object,
                  metaclass=Meta):

    """Alternative to numpy structured arrays.

    """

    def __init__(self,
                 dictdata,
                 dicttypes):
        
        """
        Data must be passed as dict somehow, to allow for:
        1. different types
        2. mapping to the space
        # """

        self._types = dicttypes
        self._data = {key: np.array(value, dtype=np.dtype(dicttypes[key])) for key, value in dictdata.items() if key in self._types.keys()}

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
 
    def __len__(self):

        return np.array([len(arr) for arr in self._data.values()][0])
    
    def __getitem__(self,
                    items):
        
        """Gets only 1 item."""
        
        #items = np.asarray(items)
        #return [self._data[item] for item in items] # return list of np arrays
        key = np.asarray(items).flatten().item()

        return self._data[key]
    
    def values(self):

        return self._data.values()
    
    @property
    def names(self):

        return list(self._data.keys())
    
    def filter(self,
               **kwargs):
        
        basis_idx = np.array([np.isin(self._data[str(variable)], condition) for variable, condition in kwargs.items()])

        #print(basis_idx)
        #idx = np.array([all(tup) for tup in basis_idx])

        return basis_idx


