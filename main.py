import numpy as np

from finstruct.structure import Structure
from finstruct.unit import TermUnit, RateUnit, DateUnit
from finstruct.basis import Space

coords_unit = [TermUnit("D"), DateUnit()]
values_unit = RateUnit("SPOT")
basis = Space(coords_unit, values_unit)
coords = [(1, np.datetime64("2010-01-01")), (10, np.datetime64("2010-01-01"))]
values = [0.01, 0.015]
struct = Structure(coords, values, basis)
results = struct.filter(term=1, date=np.datetime64("2010-01-01"))
print(results)

