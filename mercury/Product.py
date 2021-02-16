# We're using annotations in a class with functions returning
# an instance of the class inside the class.
# This will become the default behaviour starting from Python 3.10
from __future__ import annotations

import pandas as pd
import numpy as np
from datetime import datetime

from .common import ISIN,time_interval

class Product(pd.DataFrame):
    """Product."""

    def __init__(self, isin: ISIN, product_type: str, *args, data_source='unknown', **kwargs):
        self.__dict__['ISIN'] = isin
        self.product_type = product_type
        super().__init__(*args, **kwargs)

        #add required columns to dataframe
        required_columns=['Open','High','Low','Close','Volume']
        i=0
        for column in required_columns:
            if column not in super().columns:
                super().insert(i,column,np.nan)
            i = i+1

    def __setattr__(self, name, value):
        if name == "ISIN":
            raise AttributeError("Cannot change ISIN value")
        super().__dict__[name] = value

    def __repr__(self):
        return 'ISIN: {}\n\n'.format(self.ISIN) + super().__repr__()

    def at(self, instant: datetime) -> float:
        return super().at[instant, 'Close']

    def slice(self, interval : time_interval) -> Product:
        try:
            return self[interval.start:interval.end]
        except:
            return self

