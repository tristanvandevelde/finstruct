import numpy as np

def TYPECHECK(item,
              required_type) -> bool:
    
    if type(item) is not type(required_type):
        raise ValueError("Type not recognized")


def SIZECHECK(item):

    pass

def DIMCHECK(item):

    pass

import enum

class EnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True