

class Meta(type):

    """
    Adds the __validate__ method to each class, and executes it after the initialization.
    """

    def __validate__(self) -> None:

        pass
    
    @classmethod
    def __prepare__(mcs, name, bases):

        namespace = {
            **super().__prepare__(mcs, name, bases),
            "__validate__": mcs.__validate__
        }

        return namespace
         
    def __call__(cls, *args, **kwargs):

        obj = super(Meta, cls).__call__(*args, **kwargs)
        obj.__validate__()

        return obj

from collections import defaultdict

dimnames = ["Basis", "Projection"]
subdict = defaultdict(
    lambda: [],
    dimnames
)

class FixedDict(object):
        def __init__(self, dictionary):
            self._dictionary = dictionary
        def __setitem__(self, key, item):
                if key not in self._dictionary:
                    raise KeyError("The key {} is not defined.".format(key))
                self._dictionary[key] = item
        def __getitem__(self, key):
            return self._dictionary[key]
