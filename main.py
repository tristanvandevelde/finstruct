
from numbers import Number

from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver, IRCurveDriver, VOLSurfaceDriver
from finstruct.structures.structure import Structure, StructArray
from finstruct.structures.curve import IRCurve
from finstruct.structures.surface import VOLSurface

import datetime

import numpy as np


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


driver = IRCurveDriver(Basis=[DateUnit("30/360"),TermUnit("Y", "30/360")],
                       Projection=[RateUnit("SPOT", "LINEAR", "Y")])

coords = {"Date":
        [np.datetime64(datetime.date(2000,1,1)),
        np.datetime64(datetime.date(2000,1,1))],
        "Term":
        [1, 10]}

vals = {"Rate": [
    [0.1],
    [0.01]
]}

struct = Structure(coords, vals, driver=driver, name="Teststruct")


struct.idx(Term=[1])