from finstruct.core.unit import DateUnit, TermUnit
from finstruct.core.space import Space

import numpy as np

dunit = TermUnit("M", "30/360")
print(dunit)
dunit.change(TermConvention="Y", DateConvention="ACT/360")
print(dunit)