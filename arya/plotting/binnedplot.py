import seaborn as sns
import matplotlib.pyplot as plt
from seaborn._docstrings import DocstringComponents, _core_docs
from scipy.stats import binned_statistic
import astropy.stats
import numpy as np


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





def binnedplot(data, 
               x=None, y=None, 
               bins=None, binwidth=None, binrange=None,
               stat="mean", errorbar="std",
               marker="o", markersize=None,
               linestyle=None,
               log_scale=False,
               capstyle="_",
               capalpha=0.5,
               capsize=None, # todo
               errorbar_linewidth=0,
               cmin=0,
               ax=None,
               color=None,
               **kwargs
               ):
    """
    Creates a binned scatter plot. For each bin in x, 
    the chosen stat is plotted.

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

    if ax is None:
        ax = plt.gca()

    if isinstance(x, str):
        x_dat = data[x]
    else:
        raise NotImplementedError

    if isinstance(y, str):
        y_dat = data[y]
    else:
        raise NotImplementedError


    filt = ~(np.isnan(x_dat) | np.isnan(y_dat))
    x_dat = x_dat[filt]
    y_dat = y_dat[filt]

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
    # calculate stats


    if errorbar is not None:
        y_l, y_c, y_h = _binned_stat_range(x_dat, y_dat, bins, 
                                           stat=stat, errorbar=errorbar)
    else:
        y_c = _binned_stat(x_dat, y_dat, bins, stat=stat)
        y_l = None
        y_h = None

    if cmin > 0:
        filt = _binned_stat(x_dat, y_dat, bins, stat="count") > cmin
        y_c = y_c[filt]
        y_l = y_l[filt]
        y_h = y_h[filt]
        bin_centers = bin_centers[filt]


    if color is None:
        color = next(ax._get_lines.prop_cycler)["color"]

    if marker is not None:
        plt.scatter(bin_centers, y_c, marker=marker, color=color, **kwargs)

    if linestyle is not None:
        plt.plot(bin_centers, y_c, linestyle=linestyle, color=color, **kwargs)


    if y_l is not None and capstyle is not None:
        plt.scatter(bin_centers, y_l, marker=capstyle, color=color)

    if y_h is not None and capstyle is not None:
        plt.scatter(bin_centers, y_h, marker=capstyle, color=color)

    if errorbar_linewidth != 0:
        plt.vlines(bin_centers, y_l, y_h, linewidth=errorbar_linewidth,
                   color=color)


