import matplotlib as mpl
import os
import seaborn as sns
import itertools
import matplotlib.pyplot as plt

from .cmap import get_cmap


# the smallest plot elements should be 0.3pt \approx 0.1mm
# for a paper, we want fonts 10/12/14

COLORS = ["#0173b2", "#de8f05", "#029e73", "#d55e00", "#cc78bc", 
          "#ca9161", "#fbafe4", "#949494", "#ece133", "#56b4e9"]

MARKERS = ["o", "+", "^", "*", 
           "o", "s", "d", "x", "1", "v"]
FILL =    [True, True, True, True,
           False, False, False, True, True, True]

FIG_SIZE = (10/3, 10/4)



def init():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    style = "journal"

    path = os.path.join(dir_path, style + ".mplstyle")
    mpl.style.use(path)

    mpl.ticker.AutoLocator.__init__ = AutoLocatorInit

    color_cycle = mpl.cycler(color = COLORS)
    set_seaborn()

    mpl.rcParams['axes.prop_cycle'] = color_cycle

    if "arya" not in mpl.colormaps.keys():
        mpl.colormaps.register(get_cmap(), name="arya")
        mpl.colormaps.register(get_cmap(reverse=True), name="arya_r")

        mpl.colormaps.register(get_cmap(to_white=True), name="arya_w")
        mpl.colormaps.register(get_cmap(reverse=True, to_white=True), 
                               name="arya_wr")


    set_fontsize(10)
    set_linewidths(1, 2.5) # the em-dash is 10pt x 0.5pt for 10pt times
    set_tick_lengths(10/3, 10/6)
    mpl.rcParams["patch.edgecolor"] = "none"
    mpl.rcParams["hist.bins"] = 50


def get_size():
    global FIG_SIZE
    return FIG_SIZE

def set_size(s):
    global FIG_SIZE
    FIG_SIZE = s
    
    
def set_fontsize(medium, small=None, large=None):
    if small is None:
        small = 0.8*medium
        
    if large is None:
        large = 1.2*medium

    mpl.rcParams["font.size"] =  medium
    mpl.rcParams["figure.titlesize"] =  medium
    # mpl.rcParams["figure.labelsize"] =  medium
    mpl.rcParams["axes.titlesize"] = small
    mpl.rcParams["axes.labelsize"] = medium
    mpl.rcParams["xtick.labelsize"] = small
    mpl.rcParams["ytick.labelsize"] = small
    mpl.rcParams["legend.fontsize"] = medium


def set_linewidths(lw, ms):
    mpl.rcParams["lines.linewidth"] = lw
    mpl.rcParams["axes.linewidth"] = lw
    mpl.rcParams["lines.markersize"] = ms
    mpl.rcParams["errorbar.capsize"] = ms
    mpl.rcParams["xtick.major.width"] = lw
    mpl.rcParams["ytick.major.width"] = lw
    mpl.rcParams["xtick.minor.width"] = lw/2
    mpl.rcParams["ytick.minor.width"] = lw/2


def set_tick_lengths(L, l):
    mpl.rcParams["xtick.major.size"] = L
    mpl.rcParams["ytick.major.size"] = L

    mpl.rcParams["xtick.minor.size"] = l
    mpl.rcParams["ytick.minor.size"] = l


def set_seaborn():
    sns.set_style("ticks")

    sns.set_style({
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.top': True,
        'ytick.right': True,
        'axes.splines.top': True,
        'axes.splines.right': True,
        'image.cmap': 'arya',
    })

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times"



def reset_markers():


    m_cycle = []
    for i in range(10):
        kwargs = {}
        kwargs["color"] = COLORS[i]
        if not FILL[i]:
            kwargs["facecolor"] = "none"
            kwargs["edgecolor"] = COLORS[i]
        kwargs["marker"] = MARKERS[i]

        m_cycle.append(kwargs)


    global MARKER_CYCLE 
    MARKER_CYCLE = itertools.cycle(m_cycle)


def next_marker():
    return next(MARKER_CYCLE)



# override default tick locator to avoid 2.5 ticks
def AutoLocatorInit(self):
    mpl.ticker.MaxNLocator.__init__(self,
            nbins = "auto",
            steps = [1,2,5,10])


init()

# locator for linear scales but with log variables (0.2, 0.3, 0.5, and 1 are preferred step sizes)
