# import csv

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from finstruct.utils.types import Meta
from finstruct.core.driver import IRCurveDriver
from finstruct.structures.structure import Structure

class IRCurve(Structure,
              metaclass=Meta):

    """Interest Rate Curve class. 

    Attributes
    ----------

    Methods
    -------
    
    """

    _DRIVERTYPE = IRCurveDriver
    _DEFAULTDRIVER = "IRCurveDefault"

    def __init__(self,
                 data_coords,
                 data_vals,
                 driver: IRCurveDriver,
                 name = None) -> None:
        
        super().__init__(data_coords, data_vals, driver, name)

    def plot(self,
             type: str,
             **kwargs) -> None:
        
        kwargs = {key: value for key, value in kwargs.items() if key in ["Term", "Date"]}
        
        match type:
            case "history":
                """
                Plot the historical evolution of the rates.
                """
                # fix color for terms
                try:
                    terms = list(kwargs["Terms"])
                except:
                    terms = np.unique(self._coords._data["Term"])
                finally:
                    for term in terms:
                        idx = self._idx(Term=term)
                        plt.plot(self._coords.select(idx)["Date"], self._vals.select(idx)["Rate"], label=term)
                    plt.legend()
                    plt.title(self.name)
                    plt.show()

            case "termstructure":
                """
                Plot the term structure of the rates.
                """
                date = kwargs["Date"]
                terms = np.arange(1, 31)

                data = self.get_values(Date=date, Term=terms)
                terms = np.array([point["Term"] for point in data]).flatten()
                rates = np.array([point["Rate"] for point in data]).flatten()

                ## TODO: Fix why rates are stored in singletons




                plt.plot(terms, rates)
                plt.show()

                #     if len(dates) != 1:
                #      raise ValueError("Can only plot for 1 date")
                # except:
                #     raise ValueError("No date given.")
                # finally:

                    #for date in dates:
                # idx = self._idx(Date=date)
                # terms = self._coords.select(idx)["Term"]
                # rates = self._vals.select(idx)["Rate"]
                # plt.plot(terms, rates, label=date)
                # plt.legend()
                # plt.title(self.name)
                # plt.show()



#     def get_fwd(self,
#                 terms: npt.ArrayLike,
#                 dates: npt.ArrayLike):
        
#         """
#         Given two moments a and b, with b<a, the forward rate is calculated as:
#         ((1 + ra)^ta / (1 + rb)^tb) - 1
#         """

#         return None
    
#     def get_disc(self,
#                  terms: npt.ArrayLike,
#                  dates: npt.ArrayLike):
        
#         """
#         Returns the discount factors for given term points.
#         """
        
#         spot_rates = self.get_values(terms=terms)
#         disc_factors = 1/np.power(1 + spot_rates, terms)

#         return disc_factors
    





# class Spread:

#     pass

