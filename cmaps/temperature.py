import matplotlib as mpl
import numpy as np


class TemperatureCmap(object):
    temperature_cmap = (mpl.colors.ListedColormap(
        ['#6601FF',
         '#5507FF', '#4510FF', '#2122FF', '#2222FE', '#1643FE',
         '#1169FF', '#0A90FF', '#06B5FF', '#00D9F2', '#00DCD2',
         '#00DEB7', '#00DF9C', '#01E17E', '#00E55E', '#00E939',
         '#01ED1E', '#28ED17', '#64F111', '#A2F608', '#E1F903',
         '#FFF600', '#FFEE02', '#FEE502', '#FFDE02', '#FED604',
         '#FECD05', '#FFC607', '#FFBD07', '#FFB30A', '#FFA10E',
         '#FF9210', '#FF8116', '#FF6F19', '#FF5E1E', '#FF4D25',
         '#FE3E29', '#FF2D2F', '#FF1D35', '#FE083D', '#FF017A',
         '#FF00FE'
         ]))


class TemperatureBounds(object):
    temperature_bounds = np.arange(269, 312, 1)  # kelvin
