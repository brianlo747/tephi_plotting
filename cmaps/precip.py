import matplotlib as mpl
import numpy as np


class PrecipCmap(object):
    precip_cmap = (mpl.colors.ListedColormap(
        ['#848484', '#7BB1E7', '#5093D7', '#2869BE', '#1DC918', '#FEF139', '#FF9900', '#EC3219', '#A800AB', '#FE5DFB',
         '#FFFFFF']))


class PrecipBounds(object):
    precip_rate_bounds = np.array([0.10, 0.25, 0.50, 1.00, 2.00, 4.00, 8.00, 16.00, 32.00, 64.00])
    precip_rate_bounds_with_ex = np.array([0, 0.10, 0.25, 0.50, 1.00, 2.00, 4.00, 8.00, 16.00, 32.00, 64.00, 1000.0])
