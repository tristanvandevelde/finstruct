import numpy as np

def TYPECHECK(item,
              required_type) -> bool:
    
    if type(item) is not type(required_type):
        raise ValueError("Type not recognized")


def SIZECHECK(item):

    pass

def DIMCHECK(item):

    pass

print(type(np.array))