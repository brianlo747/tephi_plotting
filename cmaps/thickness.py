import matplotlib as mpl
import numpy as np


class ThicknessCmap(object):
    thickness_cmap = (mpl.colors.ListedColormap(
        ['#6601FF', '#520AFC', '#3717FF', '#2122FF',
         '#1457FE', '#0C8BFF', '#02C3FF', '#00DAE6',
         '#00DDBE', '#00E193', '#00E469', '#00E83C',
         '#07EC1D', '#5BF010', '#AFF40A', '#FBFA00',
         '#FFEF03', '#FFE206', '#FFD703', '#FECD07',
         '#FFC207', '#FFB70A', '#FFA00E', '#FE8A11',
         '#FF7518', '#FF5C1E', '#FF4627', '#FE2D31',
         '#FF1838', '#FE0152', '#FF01FE'
         ]))

    # .with_extremes(over='red', under='blue'))


class ThicknessBounds(object):
    thickness_1000_500_bounds = np.arange(486, 678, 6)
