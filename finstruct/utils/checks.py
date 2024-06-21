def TYPECHECK(item,
              required_type) -> bool:
    
    # TODO: Extend to list of allowed types

    if type(item) is not type(required_type):
        raise ValueError("Type not recognized")
    
    return True


def SIZECHECK(item):

    pass

def DIMCHECK(item):

    pass