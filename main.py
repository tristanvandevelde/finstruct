
from numbers import Number

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver, IRCurveDriver, VOLSurfaceDriver
from finstruct.structures.core import Structure, StructArray
from finstruct.structures.curve import IRCurve

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style("whitegrid")

# import configparser

# config = configparser.ConfigParser()
# config.optionxform = str



driver = IRCurveDriver(
    Index=[DateUnit("30/360")],
    Basis=[TermUnit("Y", "30/360")],
    Projection=[RateUnit("SPOT", "LINEAR", "Y")])



curve = Structure.read_csv("data/treasury_rates.csv", driver)

mydate = np.datetime64(datetime.date(2024,6,18))
mydate2 = np.datetime64(datetime.date(2024,6,14))


idx = curve._idx(Date=mydate)

terms = np.arange(1, 31)
# terms_new, rates_new = curve._interpolate(Date=np.datetime64(datetime.date(2024,6,18)), Term=terms)
index, coords, values = curve._interpolate(Date=[mydate, mydate2], Term=terms)

#print(mydate in curve._index["Date"])

df = pd.DataFrame({"Date": index.flatten(),
                   "Term": coords.flatten(),
                   "Rate": values.flatten()})

print(df)

sns.lineplot(df,
             x="Term",
             y="Rate",
             hue="Date")
plt.show()


#print(test)
#print(rates_new)
#plt.plot(terms_new, rates_new)
#plt.show()
#print(test)
#print(coords)