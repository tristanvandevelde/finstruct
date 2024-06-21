def TYPECHECK(item,
              required_type) -> bool:
    
    # TODO: Extend to list of allowed types

    if not isinstance(item, required_type):
        raise ValueError(f"Wrong type. {type(item)} should be {required_type}")
    
    return True


def SIZECHECK(item):

    pass

def DIMCHECK(item):

    pass