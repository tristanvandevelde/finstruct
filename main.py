
from numbers import Number

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver, IRCurveDriver, VOLSurfaceDriver
from finstruct.structures.structure import Structure, StructArray
from finstruct.structures.curve import IRCurve
#from finstruct.structures.surface import VOLSurface

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# import configparser

# config = configparser.ConfigParser()
# config.optionxform = str

# config.read("config/drivers/IRCurve.ini")

# # get general
# general = dict(config["General"].items())
# cls = globals()[general["type"]]
# objname = general["name"]
# if not issubclass(cls, Driver):
#     raise ValueError("Class is not Driverclass.")

# # get spaces
# space_sections = config.sections()
# space_sections.remove("General")
# for section in space_sections:
#     print(config[section].name)
#     testsec = {config[section].name: "Testing"}
#     units = dict(config[section])
#     for unittype, unitconventions in units.items():
#         print(unittype)
#         #print(type(unitconventions))
#         #print(unitconventions.split(", "))
#         print(unitconventions.split(", "))


# driver = IRCurveDriver(
#     Index=[DateUnit("30/360")],
#     Basis=[TermUnit("Y", "30/360")],
#     Projection=[RateUnit("SPOT", "LINEAR", "Y")])

# data = [
#     {
#         "Date": np.datetime64(datetime.date(2010,1,1)),
#         "Term": 10,
#         "Rate": 0.01
#     },
#         {
#         "Date": np.datetime64(datetime.date(2010,1,1)),
#         "Term": 30,
#         "Rate": 0.015
#     }
# ]

# curve = Structure.read_csv("data/treasury_rates.csv", driver)
# idx = curve._idx(Date=np.datetime64(datetime.date(2024,6,18)))

# terms = np.arange(1, 31)
# rates_new = curve._interp(Date=np.datetime64(datetime.date(2024,6,18)), Term=terms)

# plt.plot(terms, rates_new)
# plt.show()


driver = IRCurveDriver(Basis=[DateUnit("30/360"),TermUnit("Y", "30/360")],
                        Projection=[RateUnit("SPOT", "LINEAR", "Y")],
                        Index=[])
    
