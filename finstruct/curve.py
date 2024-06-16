import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from finstruct.structure import Basis, Driver
from finstruct.unit import TermUnit, DateUnit, RateUnit


class IRCurve(Driver):

    DEFAULTS = { "BASIS": Basis([DateUnit(), TermUnit("D")], RateUnit("SPOT"))}
           

    def __init__(self,
                 coords,
                 data,
                 basis: Basis = None):
        
        super().__init__(coords, data, basis)

    def get_fwd(self,
                terms):
        
        """
        Given two moments a and b, with b<a, the forward rate is calculated as:
        ((1 + ra)^ta / (1 + rb)^tb) - 1
        """

        return None
    
    def get_disc(self,
                 terms: npt.ArrayLike):
        
        """
        Returns the discount factors for given term points.
        """
        
        spot_rates = self.get_values(terms=terms)
        disc_factors = 1/np.power(1 + spot_rates, terms)

        return disc_factors
    
    def plot(self,
             date: np.datetime64):
        
        idx = self.idx(date=date)
        coords = self.coords[idx].view(np.float64)
        values = self.values[idx].view(np.float64)

        plt.plot(coords, values)
        plt.show()