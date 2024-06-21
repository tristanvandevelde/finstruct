from typing import Any

#from finstruct.utils.checks import TYPECHECK
#from finstruct.driver import Driver


class Basis:

    """
    Class to hold connection between drivers.
    """

    def __init__(self,
                 *args) -> None:
        
        self.drivers = args
        print("test")

        self.__validate__()

    def __validate__(self):

        return True


    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)
    
    def __repr__(self):
        
        #self.keys()
        return "Basis([{}])".format([repr(driver) for driver in self.drivers])

    def __str__(self):
        pass


class TestClass:

    def __init__(self, name):

        self.name = name
        self.test = 1

test = Basis(TestClass("dim1"), TestClass("dim2"))
#test = Basis()
print(repr(test))
