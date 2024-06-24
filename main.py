"""File to be used for quick-and-dirty testing."""
from finstruct.core.conventions import DaycountConvention, TermConvention, RateConvention, CompoundingConvention

#print(DaycountConvention.)

for convention in DaycountConvention:
    print(convention.name)
    print(convention.value)