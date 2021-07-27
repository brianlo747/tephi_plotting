import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable


class _PlotCollection:
    """
    Container for tephigram isopleths.
    Manages the creation and plotting of all tephigram isobars, mixing ratio
    lines and pseudo saturated wet adiabats.
    """

    def __init__(
            self,
            axes,
            spec,
            stop,
            plot_func,
            text_kwargs,
            fixed=None,
            minimum=None,
            xfocus=None,
    ):
        if isinstance(stop, Iterable):

            items = [
                [step, zoom, set(stop[step - 1:: step])]
                for step, zoom in sorted(spec, reverse=True)
            ]
        else:

            items = [
                [step, zoom, set(range(step, stop + step, step))]
                for step, zoom in sorted(spec, reverse=True)
            ]

        for index, item in enumerate(items):
            if minimum:
                item[2] = set([value for value in item[2] if value >= minimum])

            for subitem in items[index + 1:]:
                subitem[2] -= item[2]

        self.groups = {
            item[0]: _PlotGroup(
                axes, plot_func, text_kwargs, *item, fixed=fixed, xfocus=xfocus
            )
            for item in items
            if item[2]
        }

        if not self.groups:
            emsg = "The plot collection failed to generate any plot groups"
            raise ValueError(emsg)

    def refresh(self, zoom, xy_point):
        """
        Refresh all isopleth groups within the plot collection.
        Args:
        * zoom:
            Zoom level of the current plot, relative to the initial plot.
        * xy_point:
            The center point of the current plot, transformed into
            temperature and potential temperature.
        Returns:
            Boolean, whether any plot group has changed.
        """
        changed = False

        for group in self.groups.values():
            changed = group.refresh(zoom, xy_point) or changed

        return changed
