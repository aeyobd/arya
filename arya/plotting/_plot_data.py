from seaborn._core import typing
import pandas as pd
import numpy as np


class PlotData:
    def __init__(self, data, x=None, y=None, hue=None, size=None, style=None):
        self._vars = {}
        self._data = pd.DataFrame()

        for var, name in [(x, "x"), 
                (y, "y"), 
                (hue, "hue"), 
                (size, "size"), 
                (style, "style")]:

            if var is None:
                continue
            self._data[name] = data[var]
            self._vars[name] = var

        self._data.dropna()




    @property
    def data(self):
        return self._data

    @property
    def vars(self):
        return self._vars

    def __getitem__(self, key):
        return self.data[key]


