
from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver


driver = Driver([DateUnit("30/360"), TermUnit("Y", "30/360")], [RateUnit("SPOT", "LINEAR", "Y")])

print(driver.Basis)