import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy.stats import binned_statistic
import astropy.stats

from ._plot_data import PlotData


class BinnedData(PlotData):
    def __init__(self, data, x=None, y=None, hue=None, style=None, size=None,
            bins=None, binwidth=None, binrange=None,
            hue_bins=None, hue_binwidth=None, hue_binrange=None,
            stat="mean", errorbar="std",
            ):
        
        super().__init__(data, x=x, y=y, hue=hue, style=style, size=size)
        self.group_cols = list(set(["hue", "style", "size"]) & set(self.vars.keys()))

        # if hue is binned
        if ((hue is not None)
                and (hue_bins is not None 
                or (hue_binrange is not None) 
                or (hue_binwidth is not None))
            ):
            self.bin_hues(hue_bins, hue_binrange, hue_binwidth)
                

        self.bins, self.bin_centers = make_bins(
                self.data["x"], 
                bins=bins, binrange=binrange, binwidth=binwidth)

        df = pd.DataFrame()
        for group in self.groups():
            df = pd.concat([df, self.make_binned(group, stat, errorbar)], 
                           ignore_index=True)

        self._data = df
            

    def make_binned(self, df, stat, errorbar):
        data = pd.DataFrame()
        data["x"] = self.bin_centers
        if errorbar is not None:
            y_l, y_bin, y_h = _binned_stat_range(self.data.x, self.data.y, self.bins, 
                                               stat=stat, errorbar=errorbar)
            data["y_l"] = y_l
            data["y_h"] = y_h
        else:
            y_bin = _binned_stat(self.data.x, self.data.y, self.bins, stat=stat)

        data["y"] = y_bin
        for col in self.group_cols:
            data[col] = _binned_stat(self.data.x, self.data[col], self.bins, stat="mean")

        return data


    def groups(self):

        if len(self.group_cols) == 0:
            return [self.data]
        else:
            return [g for g, _ in self.data.groupby(self.group_cols)]


    def bin_hues(bins, binnrange, binwidth):
        hue_bins, hue_centers = make_bins(x_dat, bins, binrange, binwidth)
        self.hue_bines = hue_bins

        cat_filts = [
                (c_dat >= cbins[i]) & (c_dat < cbins[i+1])
                for i in range(len(c_dat))
                ]


        for cat, filt in zip(cats, cat_filts):
            self.data[filt]["hue"] = cat





def binnedplot(data, 
               x=None, y=None, 
               hue=None, style=None, size=None,
               bins=None, binwidth=None, binrange=None,
               hue_bins=None, hue_binwidth=None, hue_binrange=None,
               stat="mean", errorbar="std",
               marker="o", markersize=None,
               linestyle=None,
               log_scale=False,
               capstyle="_", capalpha=0.5, capsize=None,
               cmin=0,
               ax=None,
               color=None,
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
    dat = BinnedData(data, x=x, y=y, hue=hue, style=style, size=size,
                bins=bins, binwidth=binwidth, binrange=binrange,
                hue_bins=hue_bins, hue_binwidth=hue_binwidth, 
                hue_binrange=hue_binrange,
                stat=stat, errorbar=errorbar,
                )

    if hue is not None:
        hue = "hue"
    if size is not None:
        size = "size"
    if style is not None:
        style = "style"

    ax = sns.scatterplot(dat.data, x="x", y="y", hue=hue, size=size, style=style, **kwargs)

    if "y_l" in dat.data.keys():
        colors = ax.collections[-1].get_facecolors()
        if len(colors) == len(dat.data):
            plt.scatter(dat.data.x, dat.data.y_l, marker=capstyle, c=colors)
            plt.scatter(dat.data.x, dat.data.y_h, marker=capstyle, c=colors)
        else:
            color = colors[0]
            plt.scatter(dat.data.x, dat.data.y_l, marker=capstyle, color=color)
            plt.scatter(dat.data.x, dat.data.y_h, marker=capstyle, color=color)




def make_bins(x_dat, bins=None, binrange=None, binwidth=None):
    if binrange is None:
        binrange = (min(x_dat), max(x_dat))

    if bins is None:
        if binwidth is None:
            _, bins = astropy.stats.histogram(x_dat, range=binrange, bins="blocks")
        else:
            bins = np.arange(binrange[0], binrange[1], binwidth)

    elif isinstance(bins, int):
        bins = np.linspace(binrange[0], binrange[1], bins)

    bin_centers = (bins[1:] + bins[:-1])/2

    return bins, bin_centers


def _binned_stat(x, y, bins, stat="count", percentile=None):
    """
    Calculates statistics for the vecors x, y over the given bins. 
    """
    if percentile is not None:
        return binned_statistic(x, y,
                    statistic=lambda a: np.percentile(a, percentile), bins=bins)[0]

    if stat == "count":
        return binned_statistic(x, y, bins=bins, statistic="count")[0]
    elif stat == "mean":
        return binned_statistic(x, y, bins=bins, statistic="mean")[0]
    elif stat == "median":
        return binned_statistic(x, y, bins=bins, statistic="median")[0]
    elif stat == "std":
        return binned_statistic(x, y, bins=bins, statistic="std")[0]
    elif stat == "count":
        return binned_statistic(x, y, bins=bins, statistic="count")[0]


    raise NotImplementedError


def _binned_stat_range(x, y, bins, stat="count", errorbar="std"):
    """
    Calculates statistics for the vecors x, y over the given bins. 
    Returns xl, xc, xh, where xl and xh are the lower and upper
    values based on the errorbar setting.
    """
    if stat == "count":
        x_c = _binned_stat(x, y, bins=bins, stat="count")
        if errorbar == "std":
            e = np.sqrt(x_c)
            x_l = x_c - e
            x_h = x_c + e
            return x_l, x_c, x_h

    elif stat == "mean":
        x_c = _binned_stat(x, y, bins=bins, stat="mean")
        if errorbar == "std":
            e = _binned_stat(x, y, bins=bins, stat="std")
            x_l = x_c - e
            x_h = x_c + e
            return x_l, x_c, x_h
        elif errorbar == "sterr":
            e = _binned_stat(x, y, bins=bins, stat="std")
            c = _binned_stat(x, y, bins=bins, stat="count")
            e /= np.sqrt(c)
            x_l = x_c - e
            x_h = x_c + e
            return x_l, x_c, x_h

    elif stat == "median":
        x_c = _binned_stat(x, y, bins=bins, stat="median")
        if errorbar == "pi":
            x_l = _binned_stat(x, y, bins=bins, percentile=16)
            x_h = _binned_stat(x, y, bins=bins, percentile=84)
            return x_l, x_c, x_h

    raise NotImplementedError

