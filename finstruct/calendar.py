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
                 #data: npt.ArrayLike,   # list of dicts
                 dates,
                 values,
                 units: npt.ArrayLike = None):

        # Assert length and all that stuff
        self.dtypes = np.dtype([("date", "datetime64[D]"), ("amount", "f4")])
        self.data = np.array(list(zip(dates, values)), dtype=self.dtypes)

    @classmethod
    def read_csv(cls,
                 file):
        
        """
        Create Calendar object from a .csv-file.
        """
        
        with open(file=file, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)

        dates = [row["Date"] for row in data]
        values = [row["Cashflow"] for row in data]
        
        return cls(dates, values)

    def get_npv(self,
                curve,
                date):

        # get timedelta
        # get discount factor of timedelta
        # multiply with cashflow
        # multiply with numeraire

        disc_factor = 1/1.2
        date = datetime.date(2000, 1, 1)
    
    def get_rate(self,
                 prices):
  
        pass
