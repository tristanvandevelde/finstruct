import os, sys
sys.path.append(os.getcwd())
import datetime

import numpy as np
import pytest 

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.conventions import DaycountConvention, TermConvention
from finstruct.core.driver import Driver, IRCurveDriver
from finstruct.structures.structure import Structure

class TestStructure:
    
    def test_create(self):


        driver = IRCurveDriver(Basis=[DateUnit("30/360"),TermUnit("Y", "30/360")],
                               Projection=[RateUnit("SPOT", "LINEAR", "Y")])
        
        coords = [
            [np.datetime64(datetime.date(2000,1,1)), 1],
            [np.datetime64(datetime.date(2000,1,1)), 10]
        ]

        vals = [
            [0.1],
            [0.01]
        ]

        struct = Structure(coords, vals, driver=driver, name="Teststruct")

        assert type(struct) is Structure




if __name__ == "__main__":

    #sys.exit(pytest.main([__file__, "-c", "tests/pytest.ini"]))
    driver = IRCurveDriver(Basis=[DateUnit("30/360"),TermUnit("Y", "30/360")],
                               Projection=[RateUnit("SPOT", "LINEAR", "Y")])
        
    coords = [
        [np.datetime64(datetime.date(2000,1,1)), 1],
        [np.datetime64(datetime.date(2000,1,1)), 10]
    ]

    vals = [
        [0.1],
        [0.01]
    ]

    struct = Structure(coords, vals, driver=driver, name="Teststruct")

    #print(struct._coords.view(type=np.matrix, dtype=np.float64).reshape(struct._coords.shape + (-1,)))

    # make internal
    
    struct.set_interpolators("Term")



    struct.get_values(Term=[1,5,10],Date=np.datetime64(datetime.date(2000,1,1)))