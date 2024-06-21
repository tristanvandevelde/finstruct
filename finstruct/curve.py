import csv

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from finstruct.structure import Basis, Structure
from finstruct.unit import TermUnit, DateUnit, RateUnit


class IRCurve(Structure):

    DEFAULTS = { "BASIS": Basis([DateUnit(None), TermUnit("D")], RateUnit("SPOT"))}
           

    def __init__(self,
                 coords,
                 data,
                 basis: Basis = None):
        
        super().__init__(coords, data, basis)

    def get_fwd(self,
                terms: npt.ArrayLike,
                dates: npt.ArrayLike):
        
        """
        Given two moments a and b, with b<a, the forward rate is calculated as:
        ((1 + ra)^ta / (1 + rb)^tb) - 1
        """

        return None
    
    def get_disc(self,
                 terms: npt.ArrayLike,
                 dates: npt.ArrayLike):
        
        """
        Returns the discount factors for given term points.
        """
        
        spot_rates = self.get_values(terms=terms)
        disc_factors = 1/np.power(1 + spot_rates, terms)

        return disc_factors
    
    def plot(self,
             type: str = None,
             **kwargs):
        
        """
        
        """

        
        match type:
            case "history":
                """
                
                """
            case "termstructure":
                """
                Plot the relationship between the terms and the rates.
        
                """
            ## TODO: Implement for multiple curves way to combine these.

        idx = self.idx(date=date)
        coords = self.coords[idx].view(np.float64)
        values = self.values[idx].view(np.float64)

        plt.plot(coords, values)
        plt.show()


class IRBaseCurve(Structure):

    """
    Interest rate Base Curve class to represt a termstructure at 1 moment in time.
    """

    DEFAULTS = { "BASIS": Basis([TermUnit("Y")], RateUnit("SPOT"))}

    def __init__(self,
                 terms,
                 rates,
                 basis = None):
        
        if basis is None:
            basis = self.DEFAULTS["BASIS"]
        
        super().__init__(terms, rates, basis)

    def shift(self):
        pass

    @classmethod
    def read_csv(cls,
                 file,
                 basis = None):
        
        with open(file=file, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)

        terms = [row["term"] for row in data]
        rates = [row["rate"] for row in data]

        return cls(terms, rates, basis)
    
class IRMultiCurve:

    """
    Class to hold information about multiple curves.
    Maybe should be in a general universe-type class, allowing combination of different drivers.
    """

    pass