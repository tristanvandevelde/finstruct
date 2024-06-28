from collections.abc import MutableMapping


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

    def __validate__(self) -> None:

        pass

    ## TODO: Extend with **kwargs such that DriverMeta can inherit from it.
    # https://stackoverflow.com/questions/13762231/how-to-pass-arguments-to-the-metaclass-from-the-class-definition
    # 
    
    @classmethod
    def __prepare__(mcs, name, bases):

        namespace = {
            **super().__prepare__(mcs, name, bases),
            "__validate__": lambda self: None
        }

        return namespace
         
    def __call__(cls, *args, **kwargs):

        obj = super(Meta, cls).__call__(*args, **kwargs)
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
