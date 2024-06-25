from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.space import Space

import numpy as np

def do(**kwargs):

    print(kwargs)
    for name, value in kwargs.items():
        print(name)


do(DaycountConvention="30/360")