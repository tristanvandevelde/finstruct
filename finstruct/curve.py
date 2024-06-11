from finstruct.structure import Structure, Space
from finstruct.unit import TermUnit, DateUnit, RateUnit


class IRBaseCurve(Structure):

    DEFAULTS = {
        "BASIS": Space([TermUnit("D")], RateUnit("SPOT"))
    }


class IRHistCurve(Structure):

        DEFAULTS = {
        "BASIS": Space([DateUnit(), TermUnit("D")], RateUnit("SPOT"))
    }
        
## For the time being, implement combining methods in the curve. Maybe later to  be extended towards structure.