import numbers
import numpy as np
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from mpl_toolkits.axisartist import HostAxes, Subplot
import mpl_toolkits.axisartist.grid_finder as grid_finder
from mpl_toolkits.axisartist.grid_helper_curvelinear import (
    GridHelperCurveLinear)
from plots.radiosonde.tephigram.tephigram_transforms import *
import plots.radiosonde.tephigram.isopleths as isopleths
import plots.radiosonde.tephigram.labels as labels


class _PlotGroup():
    """
    Container for a related group of tephigram isopleths.
    Manages the creation and plotting of all isopleths within the group.
    """

    def __init__(
            self,
            axes,
            plot_func,
            levels,
            text_kwargs=None,
    ):
        self.axes = axes
        self.text_kwargs = text_kwargs
        self.levels = levels

        for level in self.levels:
            plot_func(level)

    def _generate_text(self, tag, xy_point):
        line, text = self[tag]
        x_data = line.get_xdata()
        y_data = line.get_ydata()

        if self.xfocus:
            delta = np.power(x_data - xy_point[0], 2)
        else:
            delta = np.power(x_data - xy_point[0], 2) + np.power(
                y_data - xy_point[1], 2
            )
        index = np.argmin(delta)
        text.set_position((x_data[index], y_data[index]))


class _PlotLabel():
    def __init__(
            self,
            axes,
            plot_func,
            levels,
            text_kwargs=None,
    ):
        self.axes = axes
        self.text_kwargs = text_kwargs
        self.levels = levels

        for level in self.levels:
            plot_func(level)


class Tephigram:
    """Generates a tephigram of one or more pressure and tempereature datasets."""

    def __init__(self):
        # Create figure
        self.figure = plt.figure(0, figsize=(9, 9))

        # Tephigram transformation
        self.tephi_transform = TephigramTransform()

        # grid_locator1 = grid_finder.FixedLocator(np.arange(-80, 80, 1))
        # grid_locator2 = grid_finder.FixedLocator(np.arange(-80, 80, 1))
        grid_helper = GridHelperCurveLinear(
            self.tephi_transform,
            # tick_formatter1=_FormatterIsotherm(),
            # grid_locator1=grid_locator1,
            # tick_formatter2=_FormatterTheta(),
            # grid_locator2=grid_locator2,
        )

        # Intialise subplot
        self.axes = self.figure.add_subplot(axes_class=HostAxes, grid_helper=grid_helper)

        # Configure edge axes properties
        self.axes.axis["top"].toggle(all=False)
        self.axes.axis["left"].toggle(all=False)
        self.axes.axis["bottom"].toggle(all=False)
        self.axes.axis["right"].toggle(all=False)
        self.axes.gridlines.set_linestyle("solid")

        # Drawing
        self.transform = self.tephi_transform + self.axes.transData

        # Draw isotherms
        isotherms_func = partial(isopleths.isotherm, 50, 1050, self.axes, self.transform,
                                 {"color": "#23CE1F", "linewidth": 0.05})
        _PlotGroup(self.axes, isotherms_func, np.arange(-90, 70, 1))
        isotherms_func = partial(isopleths.isotherm, 50, 1050, self.axes, self.transform,
                                 {"color": "#23CE1F", "linewidth": 0.25})
        _PlotGroup(self.axes, isotherms_func, np.arange(-90, 70, 10))

        # Draw isentropes
        isentropes_func = partial(isopleths.isentropes, -90, 70, 50, 1050, self.axes, self.transform,
                                  {"color": "#23CE1F", "linewidth": 0.05})
        _PlotGroup(self.axes, isentropes_func, np.arange(-90, 250, 10))

        # Draw isobars
        isobars_func = partial(isopleths.isobar, -90, 70, self.axes, self.transform,
                               {"color": "#23CE1F", "linewidth": 0.05})
        _PlotGroup(self.axes, isobars_func, np.arange(50, 1051, 10))
        isobars_func = partial(isopleths.isobar, -90, 70, self.axes, self.transform,
                               {"color": "#23CE1F", "linewidth": 0.25})
        _PlotGroup(self.axes, isobars_func, np.arange(100, 1051, 100))

        # Draw moist adiabats
        moist_adiabats_func = partial(isopleths.moist_adiabat, -50, 1050, 1000, self.axes, self.transform,
                                      {"color": "#23CE1F", "linewidth": 0.25})
        _PlotGroup(self.axes, moist_adiabats_func, np.arange(-40, 70, 10))

        # Draw mixing ratios
        mixing_ratios_func = partial(isopleths.mixing_ratio, -50, 50, 1050, self.axes, self.transform,
                                     {"color": "#23CE1F", "linewidth": 0.25, "linestyle": "--"})
        _PlotGroup(self.axes, mixing_ratios_func,
                   np.array([0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9,
                             10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 68, 80]))

        # Isotherm Labels
        isotherm_label_list = np.arange(-40, 70, 10)
        isotherm_label_func = partial(labels.isotherm_label, 1000, self.axes, self.transform)
        _PlotLabel(self.axes, isotherm_label_func, isotherm_label_list)

        # Isobar Labels
        isobar_label_list = np.array([50, 60, 70, 80, 90, 100, 150, 200])
        isobar_label_func = partial(labels.isobar_label, 'isotherm', -90, self.axes, self.transform)
        _PlotLabel(self.axes, isobar_label_func, isobar_label_list)

        isobar_label_list = np.array([300])
        isobar_label_func = partial(labels.isobar_label, 'isentrope', 0, self.axes, self.transform)
        _PlotLabel(self.axes, isobar_label_func, isobar_label_list)

        isobar_label_list = np.arange(400, 1050, 100)
        isobar_label_func = partial(labels.isobar_label, 'isentrope', -10, self.axes, self.transform)
        _PlotLabel(self.axes, isobar_label_func, isobar_label_list)

        # Mixing Ratio Labels
        mixing_ratio_label_list = np.array(
            [0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9,
             10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 68, 80])
        mixing_ratio_label_func = partial(labels.mixing_ratio_label, 1050, self.axes, self.transform)
        _PlotLabel(self.axes, mixing_ratio_label_func, mixing_ratio_label_list)

        # Retain aspect ratio
        self.axes.set_aspect(1.0)

        # Limits
        self.axes.set_xlim(0.5, 1.25)
        self.axes.set_ylim(-1.1, -0.2)


if __name__ == '__main__':
    Tephigram()
plt.savefig('test.pdf')
