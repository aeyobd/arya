import numpy as np
import matplotlib.pyplot as plt



def scotts_bin_width(x):
    f = np.isfinite(x)
    N = len(x)
    return 3.49 * np.std(x[f]) / np.cbrt(N)

def scotts_bins(x):
    f = np.isfinite(x)
    return np.arange(np.min(x[f]), np.nanmax(x[f]), scotts_bin_width(x))

def hist(x, bins=None, **kwargs):
    if bins is None:
        bins = scotts_bins(x)
    plt.hist(x, bins=bins, **kwargs)

def hist2d(x, y, bins=None, **kwargs):
    if bins is None:
        xbins = scotts_bins(x)
        ybins = scotts_bins(y)
        
    plt.hist2d(x, y, norm="log", bins=(xbins, ybins), **kwargs)
