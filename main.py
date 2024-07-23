
from numbers import Number
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style("whitegrid")

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver, IRCurveDriver, VOLSurfaceDriver
from finstruct.structures.core import Structure, StructArray, Manifold
from finstruct.structures.curve import IRCurve


driver = IRCurveDriver(
    Index=[DateUnit("30/360")],
    Basis=[TermUnit("Y", "30/360")],
    Projection=[RateUnit("SPOT", "LINEAR", "Y")])



curve = Manifold.read_csv("data/treasury_rates.csv", driver, name="Test Manifold")

dates = [np.datetime64(datetime.date(2024,6,18)), np.datetime64(datetime.date(2024,6,14))]
terms = np.arange(1, 31)

#idx = curve._idx(Date=dates[0], Term=1) # error here
#idx2 = curve._idx_new(Date=dates[0], Term=10)

#print(all(idx == idx2))

index, coords, values = curve._interpolate(Date=dates, Term=terms)
# print(idx)

df = pd.DataFrame({"Date": index.flatten(),
                   "Term": coords.flatten(),
                   "Rate": values.flatten()})
print(df)
sns.lineplot(df,
             x="Term",
             y="Rate",
             hue="Date")
plt.show()

testdict = {
    "a": 1,
    "b": 2
}


from finstruct.utils.data import StructArray

dictdata = {"a": [1, 2, 3],
            "b": ["a", "b", "c"]}
dicttypes = {"a": int,
             "b": str}

test = StructArray(dictdata, dicttypes)

test2 = test.filter(a=[1,2],b="a")
#print(test2._data)
#print(idx)

#print(curve.data)
