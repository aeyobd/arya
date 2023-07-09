import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy.stats import binned_statistic
import astropy.stats

from ._plot_data import PlotData
from ..figure.colorbar import Colorbar
from .binnedplot import plot_err



def medianplot(data, 
               # data and processing
               x=None, y=None, 
               hue=None, style=None, size=None,
               binsize=20,
               stat="median", errorbar="pi",
               # aesthetics
               hue_label=None,
               aes="scatter",
               legend=True,
               color=None,
               err_kwargs={},
               **kwargs
               ):
    """
    Creates a binned scatter plot. For each bin in x, 
    the chosen stat is plotted.
    then uses seaborn to create actual plot

    Params
    ------
    data :  :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        The Input data for the plot.
    x, y :  vectors or keys in ``data``
    bins : ``int`` or list-like
    binwidth
    binrange
    stat
    errorbar: 
        statistic for errorbars


    kwargs

    """
    if hue_label is None:
        hue_label=hue

    dat = MedianData(data, x=x, y=y, hue=hue, style=style, size=size,
            binsize=binsize, stat=stat, errorbar=errorbar)

    if hue is not None:
        hue = "hue"
    if size is not None:
        size = "size"
    if style is not None:
        style = "style"

    has_cb, cb = create_cb(dat, hue, hue_label, legend)

    if has_cb:
        for group in dat.groups():
            color = cb(np.mean(group.hue)) # TODO
            plot_err(group, color=color, aes=aes, err_kwargs=err_kwargs, **kwargs)
    else:
        for group in dat.groups():
            if color is None:
                color = next(plt.gca()._get_lines.prop_cycler)["color"]
            plot_err(group, color=color, aes=aes, err_kwargs=err_kwargs, **kwargs)


    if has_cb or not legend:
        plt.gca().legend().remove()


    return dat


def create_cb(dat, hue, hue_label, legend):
    # binned_hue = (hue_bins is not None) or (hue_binwidth is not None) or (hue_binrange is not None)
    binned_hue = False
    if (hue is not None) and (len(dat.data.hue.unique()) > 2):
        if binned_hue:
            if hue_binrange is None:
                hue_binrange = (min(dat.data.hue), max(dat.data.hue))
            cb = Colorbar(hue_binrange, norm=dat.hue_bins,
                          label=hue_label, create=legend)
        else: 
            cb = Colorbar((min(dat.data.hue), max(dat.data.hue)), label=hue_label,
                          create=legend)
        seq_hue = True
    else:
        seq_hue = False
        cb = None

    return seq_hue, cb



class MedianData(PlotData):
    def __init__(self, data, x=None, y=None, 
            hue=None, style=None, size=None, **kwargs):
        
        super().__init__(data, x=x, y=y, hue=hue, style=style, size=size)

        self.group_cols = list(set(["hue", "style", "size"]) & set(self.vars.keys()))

        df = pd.DataFrame()
        
        for group in self.groups():
            df = pd.concat(
                     [df, self.bin(group,  **kwargs)], 
                     ignore_index=True)

        self._old_data = data
        self._data = df


    def bin(self, df, stat, binsize=10, errorbar=None):
        df_sorted = df.sort_values(by="x")

        self.has_errors = errorbar is not None


        N = len(df_sorted) 
        offset = (N % binsize)//2

        if self.has_errors:
            data = pd.DataFrame(columns=["x", "y", "y_l", "y_h"])
        else:
            data = pd.DataFrame(columns=["x", "y"])

        i = 0
        while i + 2*binsize < N:
            if i == 0:
                j = i + binsize + offset
            elif i > N - 2*binsize + offset:
                j = -1
            else:
                j = i + binsize

            group = df_sorted.iloc[i:j]

            x = _stat(group["x"], stat)
            y = _stat(group["y"], stat)

            print(x)
            print(y)
            if self.has_errors:
                y_l, y_h = _stat_range(df.y, stat=stat, errorbar=errorbar)
                data = pd.concat([data, pd.DataFrame(
                    dict(x=[x], y=[y], y_l=[y_l], y_h=[y_h]))],
                                 ignore_index=True)
            else:
                data = pd.concat([data, pd.DataFrame(dict(x=[x], y=[y]))],
                                 ignore_index=True)

            i += binsize

        print(data)
        return data


    def groups(self):
        if len(self.group_cols) == 0:
            return [self.data]

        gs = []
        for _, g in self.data.groupby(self.group_cols):
            if len(g) > 0:
                gs.append(g)

        print(gs)
        return gs



    @property
    def x(self):
        return self.data["x"]

    @property
    def y(self):
        return self.data["y"]

    @property
    def hue(self):
        return self.data["hue"]

    @property
    def y_l(self):
        return self.data["y_l"]

    @property
    def y_h(self):
        return self.data["y_h"]








def _stat(x, stat="count", percentile=None):
    """
    Calculates statistics for the vecors x, y over the given bins. 
    """
    if percentile is not None:
        return np.percentile(x, percentile)

    if stat == "count":
        return len(x)
    elif stat == "mean":
        return np.mean(x)
    elif stat == "median":
        return np.median(x)
    elif stat == "std":
        return np.std(x)
    elif stat == "count":
        return binned_statistic(x, y, bins=bins, statistic="count")[0]
    elif stat == "mode":
        return binned_statistic(x, y, bins=bins, 
                                statistic=lambda a: max(set(a), key=list(a).count))[0]

    raise NotImplementedError



def _stat_range(x, stat="count", errorbar="std"):
    """
    Calculates statistics for the vecors x, y over the given bins. 
    Returns xl, xc, xh, where xl and xh are the lower and upper
    values based on the errorbar setting.
    """

    if stat == "mean":
        x_c = np.mean(x)
        if errorbar == "std":
            e = np.std(x)
            x_l = x_c - e
            x_h = x_c + e
            return x_l, x_h
        elif errorbar == "sterr":
            e = np.std(x)
            c = len(x)
            e /= np.sqrt(c)
            x_l = x_c - e
            x_h = x_c + e
            return x_l, x_h

    elif stat == "median":
        x_c = np.median(x)
        if errorbar == "pi":
            x_l = _stat(x, percentile=16)
            x_h = _stat(x, percentile=84)
            return x_l, x_h

    raise NotImplementedError

