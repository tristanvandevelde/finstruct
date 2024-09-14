
from finstruct.utils.types import Meta
from finstruct.core.unit import Unit


class DriverMeta(Meta):

    def __new__(metacls, name, bases, namespace, **kwargs):

        return super().__new__(metacls, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace, **kwargs):

        super().__init__(name, bases, namespace)


class Driver(metaclass=DriverMeta):

    _DIMTYPES = {"Index": [],
                 "Basis": [],
                 "Projection": []}

class ManifoldDriver(Driver):

    pass

class GridDriver(Driver):

    pass


## TODO: Q: Do Manifold and Grid need separate driver types?

## TODO: Maybe in idea, a driver should hold names and units for each variable.
## Or otherwise>

## var = Variable(Unit, name, data)
## curve = Curve(DateVariable, RateVariable, TermVariable)

# Where does the driver fit in for this one?


## Compare 2 examples:

## IR Curve
## Correlation Matrix

# Is the name on the level of the unit, driver, or structure?

# Probably only on the Structure level for Manifolds.

# However, what for the correlation matrix?

# Value: correlation
# Coord: macrovariable []

# Work with some kind of basis, where these matrices are symmetric and have the same basis twice

## --> These do require the same conventions (for example, all measured at the same moment)
## All the coords need to have the same unit probably?
## In this way. Maybe there can be grids with multiple types of units.

## Note that in this case, the correlation is derived from the price. The coordination value is not the price, but the name of the asset.

## MigrationMatrix has the same setup: CreditCategories[]

## Consider also Calendar
## Coord: date []
## Maybe extra coord?
## Value: price

## For each date, we have 1 price
## Can also be multiple values.
# For example: Date(Price, Probability)


# 1D grid: Calendar
# 2D grid: CorrelationMatrix, TransitionMatrix
# 3D grid: 

# The issue is, the values of the coords might need to be usable as keys for other objects.

# A solution can be, export a "variable type" from a manifold.

# curve = ()
# curve.variable (this contains the units and the name)

# this stuff should be handled by the driver somehow.



## Consider the correlation matrix between the prices of a few assets.
## However, it's possible they are expressed in different currencies.

# Allow each price to have its own currency.
# But also allow the consistency calculation.

# In this sense:
# Driver defines the fact that there is a price dimension,
# But does not define the unit for this entire dimension.