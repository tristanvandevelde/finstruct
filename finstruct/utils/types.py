

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