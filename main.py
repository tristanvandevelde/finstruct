from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.space import Space

import numpy as np

units = np.array([DateUnit("30/360"), TermUnit("M", "30/360")])

ctypes = [type(unit) for unit in units]

print([type(ctype) is DateUnit for ctype in ctypes])

for ctype in ctypes:
    print(ctype)

print(DateUnit)