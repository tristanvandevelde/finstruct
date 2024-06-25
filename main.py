from finstruct.core.unit import DateUnit, TermUnit, RateUnit
from finstruct.core.driver import Driver

basis = [DateUnit("30/360"), TermUnit("M", "30/360")]
projection = [RateUnit("SPOT","LINEAR","Y",1)]

driver = Driver(basis, projection)

print(driver.Basis)
print(driver.Projection)