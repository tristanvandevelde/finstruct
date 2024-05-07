import sys

import pytest

from finstruct.structure import Structure
from finstruct.unit import TermUnit, RateUnit, DateUnit
from finstruct.basis import Space



# class MyPlugin:
#     def pytest_sessionfinish(self):
#         print("*** test run reporting finishing")

#     def try_test():

#         coords_unit = [TermUnit("D"), DateUnit()]
#         values_unit = RateUnit("SPOT")
#         basis = Space(coords_unit, values_unit)
#         #print(basis)
#         coords = [1, 10]
#         values = [0.01, 0.015]
#         struct = Structure(coords, values, basis)
#         struct.filter(term=1, date='')

#         assert 2*2 == 4, ValueError("wrong implemented")

# if __name__ == "__main__":
#     sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))
#     #sys.exit(pytest.main(["-c tests/pytest.ini"]))
#     print("test")

def try_test():

    assert 2*2 == 4