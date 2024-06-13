import csv
import datetime
from finstruct.unit import DateUnit, TermUnit, DaycountUnit
import numpy as np
import numpy.typing as npt


class Calendar:

    """
    A calendar defines the exchange of cashflows on certain times with certain probabilities.
    """

    DEFAULTS = {}

    def __init__(self,
                 #data: npt.ArrayLike,   # list of dicts
                 dates: npt.ArrayLike,
                 values: npt.ArrayLike,
                 dateunit: DateUnit = None):

        self.dateunit = dateunit
        dtypes = np.dtype([("date", self.dateunit.dtype), ("amount", "f4")])
        self.data = np.array(list(zip(dates, values)), dtype=dtypes)

    @classmethod
    def read_csv(cls,
                 file,
                 dateunit):
        
        """
        Create Calendar object from a .csv-file.
        """
        
        with open(file=file, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            data = list(reader)

        dates = [row["Date"] for row in data]
        values = [row["Cashflow"] for row in data]
        
        return cls(dates, values, dateunit=dateunit)

    def get_npv(self,
                eval_date,
                curve = None):

        # get timedelta
        # get discount factor of timedelta
        # multiply with cashflow

        disc_factor = lambda x : 1/np.power(1.2, x)
        #date = datetime.date(2000, 1, 1)
        #eval_date = np.datetime64("2000-01-01", "D")
        timediff = [self.dateunit.daycount.calc_yearfraction(eval_date, end_date) for end_date in self.data["date"]]
        PVs = disc_factor(timediff) * self.data["amount"]
        #print(self.dateunit.daycount.calc_daycount(eval_date, self.data["date"]))
        #self.dateunit.daycount.calc_daycount(eval_date, )
        return np.sum(PVs)
    
    def get_rate(self,
                 prices):
  
        pass
