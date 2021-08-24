import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import cartopy.crs as ccrs


class GlobalModelPlot(object):
    """
    This class contains a plot and relevant methods for visualising relevant fields in the UKMO Global Model
    """

    def __init__(self, global_model_obj):
        self.global_model_obj = global_model_obj

    def plot_fields(self,
                    color_field,
                    output_plot_directory,
                    color_field_cmap=None,
                    color_field_cmap_bounds=None,
                    color_field_cbar_labels=None,
                    color_field_contours=False,
                    contour_field1=None,
                    contour_field1_levels=None,
                    contour_field2=None,
                    contour_field2_levels=None,
                    plot_title=None,
                    dpi=800):
        prj = ccrs.Stereographic(
            true_scale_latitude=60,
            central_longitude=-35,
            central_latitude=90)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=prj)
        # Without borders
        plt.subplots_adjust(left=0, bottom=0, right=1.0, top=1.0, wspace=None, hspace=None)
        ax.outline_patch.set_visible(False)

        cmap_norm = mpl.colors.BoundaryNorm(color_field_cmap_bounds, color_field_cmap.N)

        pcolor_plot = ax.pcolormesh(self.global_model_obj.iris_cubes[color_field].coord('longitude').points,
                                    self.global_model_obj.iris_cubes[color_field].coord('latitude').points,
                                    self.global_model_obj.iris_cubes[color_field].data, cmap=color_field_cmap,
                                    norm=cmap_norm,
                                    transform=ccrs.PlateCarree())
        if color_field_contours:
            pcolor_countours = ax.contour(self.global_model_obj.iris_cubes[color_field].coord('longitude').points,
                                          self.global_model_obj.iris_cubes[color_field].coord('latitude').points,
                                          self.global_model_obj.iris_cubes[color_field].data,
                                          levels=color_field_cmap_bounds,
                                          transform=ccrs.PlateCarree(), colors='black', linewidths=0.2)
            ax.clabel(pcolor_countours, inline=True, fontsize=5, inline_spacing=1)

        field1_countours = ax.contour(self.global_model_obj.iris_cubes[contour_field1].coord('longitude').points,
                                      self.global_model_obj.iris_cubes[contour_field1].coord('latitude').points,
                                      self.global_model_obj.iris_cubes[contour_field1].data,
                                      levels=contour_field1_levels,
                                      transform=ccrs.PlateCarree(), colors='black', linewidths=0.6)
        ax.clabel(field1_countours, inline=True, fontsize=6, inline_spacing=1, use_clabeltext=True)

        if contour_field2 is not None:
            field2_countours = ax.contour(self.global_model_obj.iris_cubes[contour_field2].coord('longitude').points,
                                          self.global_model_obj.iris_cubes[contour_field2].coord('latitude').points,
                                          self.global_model_obj.iris_cubes[contour_field2].data,
                                          levels=contour_field2_levels,
                                          transform=ccrs.PlateCarree(), colors='#00008B', linewidths=0.4)
            ax.clabel(field2_countours, inline=True, fontsize=6, inline_spacing=1, use_clabeltext=True)

        lat_lines = np.arange(20, 85, 10)
        lon_lines = np.arange(-80, 100, 10)
        ax.coastlines(resolution='50m', linewidth=0.25, color='white', zorder=2)
        gl = ax.gridlines(linewidth=0.35, color='white', alpha=1.0, zorder=1)
        gl.xlocator = mticker.FixedLocator(lon_lines)
        gl.ylocator = mticker.FixedLocator(lat_lines)
        coords = prj.transform_points(
            ccrs.PlateCarree(), np.asarray([-53.9666666667, 49.7333333333]), np.asarray([34.7166666667, 37.1166666667]))
        ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], prj)

        # Black rectangle at bottom
        ax.add_patch(Rectangle((0, 0), 1.0, 0.025, alpha=1, zorder=10, transform=ax.transAxes,
                               facecolor='black'))

        # Details in black rectangle
        datetime_obj = self.global_model_obj.iris_cubes[color_field].coord('forecast_reference_time')
        datetime_string = f"Issued: " \
                          f"{datetime_obj.units.num2date(datetime_obj.points[0]).strftime('%Y-%m-%d (%a) %H:%M:%SZ')}"
        fcst_obj = self.global_model_obj.iris_cubes[color_field].coord('time')
        fcst_string = f"{fcst_obj.units.num2date(fcst_obj.points[0]).strftime('%Y-%m-%d (%a) %H:%M:%SZ')}"
        fcst_tplus = np.round(self.global_model_obj.iris_cubes[color_field].coord('forecast_period').points[0])
        fcst_valid_string = f"{fcst_string} T+{fcst_tplus:.0f}h"
        ax.text(0.001, 0.0125, "UKMO Global",
                horizontalalignment='left',
                verticalalignment='center',
                color='white', zorder=11,
                size=5, transform=ax.transAxes)
        ax.text(0.125, 0.0125, plot_title,
                horizontalalignment='left',
                verticalalignment='center',
                color='white', zorder=11,
                size=5, transform=ax.transAxes)
        ax.text(0.750, 0.0125, datetime_string, horizontalalignment='center', verticalalignment='center',
                color='white', size=5, zorder=11,
                transform=ax.transAxes)
        ax.text(0.999, 0.0125, "UoR-Met-WCD", horizontalalignment='right', verticalalignment='center',
                color='yellow', size=5, zorder=11,
                transform=ax.transAxes)

        # Black rectangle at top left
        ax.add_patch(Rectangle((0, 1), 0.325, -0.05, alpha=1, zorder=20, transform=ax.transAxes,
                               facecolor='black'))
        ax.text(0.005, 0.975, fcst_valid_string, horizontalalignment='left', verticalalignment='center',
                color='white', size=8, zorder=21,
                transform=ax.transAxes)

        # Details in black rectangle

        # Cbar
        ax_divider = make_axes_locatable(ax)
        cax = ax_divider.append_axes("bottom", size=0.1, pad=-0.20, axes_class=mpl.pyplot.Axes, transform=ax.transAxes)
        cb = fig.colorbar(pcolor_plot, cax=cax, orientation="horizontal")
        cb.set_ticks(color_field_cbar_labels)
        cb.outline.set_visible(False)  # Remove the colorbar outline
        cb.ax.tick_params(width=0)  # Remove the colorbar ticks
        cb.ax.xaxis.set_tick_params(pad=-9.5)  # Put the colobar labels inside the colorbar
        cb.ax.tick_params(axis='x', colors='grey', labelsize=6)  # Change the color and size of the colorbar labels

        # Logo
        logo_ukmo = plt.imread('/Users/brianlo/Desktop/Reading/PhD/WCD/data/1200px-Met_Office.svg.png')
        im = OffsetImage(logo_ukmo, zoom=0.02)
        ab = AnnotationBbox(im, (0.97, 0.085), frameon=False, zorder=15, xycoords=ax.transAxes, pad=0)
        ax.add_artist(ab)

        # plt.show()
        plt.savefig(output_plot_directory, dpi=dpi,
                    bbox_inches='tight',
                    pad_inches=0)
