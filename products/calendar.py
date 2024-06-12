import csv
import datetime
#from finstruct.unit import DateUnit, TermUnit
#from .finstruct.unit import Unit, DateUnit, TermUnit
import numpy as np
import numpy.typing as npt


class Calendar:

    """
    A calendar defines the exchange of cashflows on certain times with certain probabilities.
    """

    DEFAULTS = {}

    def __init__(self,
                 data: npt.ArrayLike,   # list of dicts
                 units: npt.ArrayLike = None):

        # Assert length and all that stuff

        if units is None:
            # set defaults
            units = ["DateUnit", "MoneyUnit"]
        self.units = np.array(units)    # add dtype
        self.dtypes = np.dtype([("Date", datetime.date), ("Cashflow", float)])
        self.data = np.array([(el["Date"], el["Cashflow"]) for el in data], dtype=self.dtypes)

    @classmethod
    def read_csv(cls,
                 file):
        
        """
        Create Calendar object from a .csv-file.
        """
        
        with open(file=file, mode="r", newline="\n", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            #print(reader.fieldnames)
            data = list(reader)
        
        return cls(data)


    def get_npv(self,
                curve):


        # get timedelta
        # get discount factor of timedelta
        # multiply with cashflow
        # multiply with numeraire

        return None
    
    def get_rate(self,
                 prices):
  
        pass
