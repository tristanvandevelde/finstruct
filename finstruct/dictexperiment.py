from collections import UserDict
from typing import Any

#from finstruct.utils.checks import TYPECHECK
#from finstruct.driver import Driver

class Space(UserDict):

    """
    Alternative to basis.
    """

    # def __init__(self,
    #              drivers: dict) -> None:
        
    #     """
    #     Load in, and assert that all values are drivers.
    #     """

    def __setitem__(self, key: Any, value: Any) -> None:
            
        return super().__setitem__(key, value)