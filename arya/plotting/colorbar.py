import matplotlib as mpl
import matplotlib.pyplot as plt



class HueMap:
    def __init__(self, clim, norm):
        self.mpl_sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=clim[0],
                    vmax=clim[1], clip=False))


class Colorbar:
    def __init__(self, clim, norm="linear", ):
        pass


