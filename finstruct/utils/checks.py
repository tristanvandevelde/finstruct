def TYPECHECK(item,
              required_type) -> None:
    
    # TODO: Extend to list of allowed types

    if not isinstance(item, required_type):
        raise ValueError(f"Wrong type. {type(item)} should be {required_type}")
    
    return True


def LENCHECK(item1,
             item2) -> None:
    
    if not (len(item1) == len(item2)):
        raise ValueError(f"Wrong lengths. {item1} should be of length {item2}")
    

def SIZECHECK(item):

    pass

def DIMCHECK(item):

    pass

def SPACECHECK(space,
               units) -> None:
    
    pass