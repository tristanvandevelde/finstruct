
from finstruct.utils.checks import TYPECHECK

class Meta(type):

    """
    Adds the __validate__ method to each class, and executes it after the initialization.
    """
    
    @classmethod
    def __prepare__(mcs, name, bases):

        def __validate__(self) -> None:

            for attribute, value in self.DEFAULTS.items():
                # Set default if empty
                if getattr(self, attribute) is None:
                    setattr(self, attribute, value)
                # Check type
                if type(value) is not None:
                    TYPECHECK(getattr(self, attribute), type(value))

        namespace = {
            **super().__prepare__(mcs, name, bases),
            "__validate__": __validate__
        }

        return namespace
         
    def __call__(cls, *args, **kwargs):

        obj = super(Meta, cls).__call__(*args, **kwargs)
        obj.__validate__()

        return obj
    