import numpy as np
import pyproj
import cartopy
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import cartopy.crs as ccrs


class SatPlot(object):
    """
    This class contains a plot and relevant methods for visualising AUTOSAT files
    and one relevant field in the UKMO Global Model
    """

    def __init__(self, sat_obj, global_model_obj):
        self.sat_obj = sat_obj
        self.global_model_obj = global_model_obj

    def plot_fields(self,
                    output_plot_directory,
                    contour_field1=None,
                    contour_field1_levels=None,
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
        ax.axis('off')
        ax.outline_patch.set_visible(False)

        # For Pyproj version >=2.1.0
        # transform_latlon_to_stere = pyproj.Transformer.from_proj('epsg:4326', prj.proj4_init, always_xy=True)
        # bl_x, bl_y = transform_latlon_to_stere.transform(self.sat_obj.bl_long / 1000, self.sat_obj.bl_lat / 1000)
        # tr_x, tr_y = transform_latlon_to_stere.transform(self.sat_obj.tr_long / 1000, self.sat_obj.tr_lat / 1000)

        # For Pyproj version ==1.9.6
        proj_latlon = pyproj.Proj(init='epsg:4326', switch=False)
        proj_bng = pyproj.Proj(**prj.proj4_params, switch=False)
        bl_x, bl_y = pyproj.transform(p1=proj_latlon,
                                      p2=proj_bng,
                                      x=self.sat_obj.bl_long / 1000,
                                      y=self.sat_obj.bl_lat / 1000)
        tr_x, tr_y = pyproj.transform(p1=proj_latlon,
                                      p2=proj_bng,
                                      x=self.sat_obj.tr_long / 1000,
                                      y=self.sat_obj.tr_lat / 1000)

        lat_lines = np.arange(20, 85, 10)
        lon_lines = np.arange(-80, 100, 10)
        ax.coastlines(resolution='50m', color='white', linewidth=0.25)
        bodr = cartopy.feature.NaturalEarthFeature(category='cultural',
                                                   name='admin_0_boundary_lines_land', scale='50m', facecolor='none',
                                                   alpha=0.7)
        ax.add_feature(bodr, edgecolor='white', linewidth=0.5)
        # gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5)
        # gl.xlocator = mticker.FixedLocator(lon_lines)
        # gl.ylocator = mticker.FixedLocator(lat_lines)

        img_extent = (bl_x, tr_x, bl_y, tr_y)
        # img_extent = (-53.927, 46.778, 10.247, 33.422)
        img = self.sat_obj.sat_image
        ax.imshow(img, origin='lower', extent=img_extent, transform=prj, cmap='gist_yarg',
                  vmin=0, vmax=255, zorder=-1)
        # coords = prj.transform_points(
        #     ccrs.PlateCarree(), np.asarray([-53.9666666667, 49.7333333333]), np.asarray([34.7166666667, 37.1166666667]))
        coords = prj.transform_points(
            ccrs.PlateCarree(), np.asarray([-53.927, 46.778]), np.asarray([32.247, 33.422]))
        ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], prj)

        field1_countours = ax.contour(self.global_model_obj.iris_cubes[contour_field1].coord('longitude').points,
                                      self.global_model_obj.iris_cubes[contour_field1].coord('latitude').points,
                                      self.global_model_obj.iris_cubes[contour_field1].data,
                                      levels=contour_field1_levels,
                                      transform=ccrs.PlateCarree(), colors='yellow', linewidths=0.6)
        ax.clabel(field1_countours, inline=True, fontsize=6, inline_spacing=1, use_clabeltext=True)

        lat_lines = np.arange(20, 85, 10)
        lon_lines = np.arange(-80, 100, 10)
        ax.coastlines(resolution='50m', linewidth=0.25, color='white', zorder=2)
        gl = ax.gridlines(linewidth=0.35, color='white', alpha=1.0, zorder=1)
        gl.xlocator = mticker.FixedLocator(lon_lines)
        gl.ylocator = mticker.FixedLocator(lat_lines)
        # coords = prj.transform_points(
        #     ccrs.PlateCarree(), np.asarray([-53.9666666667, 49.7333333333]), np.asarray([34.7166666667, 37.1166666667]))
        # ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], prj)

        # Black rectangle at bottom
        ax.add_patch(Rectangle((0, 0), 1.0, 0.025, alpha=1, zorder=10, transform=ax.transAxes,
                               facecolor='black'))

        # Details in black rectangle
        # TODO: Satellite imagery time?
        datetime_obj = self.global_model_obj.iris_cubes[contour_field1].coord('forecast_reference_time')
        datetime_string = f"Issued: " \
                          f"{datetime_obj.units.num2date(datetime_obj.points[0]).strftime('%Y-%m-%d (%a) %H:%M:%SZ')}"
        fcst_obj = self.global_model_obj.iris_cubes[contour_field1].coord('time')
        fcst_string = f"{fcst_obj.units.num2date(fcst_obj.points[0]).strftime('%Y-%m-%d (%a) %H:%M:%SZ')}"
        # fcst_tplus = np.round(self.global_model_obj.iris_cubes[color_field].coord('forecast_period').points[0])
        # fcst_valid_string = f"{fcst_string} T+{fcst_tplus:.0f}h"
        ax.text(0.001, 0.0125, "Meteosat 0° IR 10.8 | UKMO Global",
                horizontalalignment='left',
                verticalalignment='center',
                color='white', zorder=11,
                size=5, transform=ax.transAxes)
        ax.text(0.250, 0.0125, plot_title,
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
        ax.add_patch(Rectangle((0, 1), 0.28, -0.05, alpha=1, zorder=20, transform=ax.transAxes,
                               facecolor='black'))
        ax.text(0.005, 0.975, fcst_string, horizontalalignment='left', verticalalignment='center',
                color='white', size=8, zorder=21,
                transform=ax.transAxes)

        # Details in black rectangle

        # Logo
        logo_ukmo = plt.imread('/Users/brianlo/Desktop/Reading/PhD/WCD/data/1200px-Met_Office_white.svg.png')
        im = OffsetImage(logo_ukmo, zoom=0.025)
        ab = AnnotationBbox(im, (0.965, 0.08), frameon=False, zorder=15, xycoords=ax.transAxes, pad=0)
        ax.add_artist(ab)

        logo_eumetsat = plt.imread('/Users/brianlo/Desktop/Reading/PhD/WCD/data/1280px-EUMETSAT_logo_white.svg.png')
        im = OffsetImage(logo_eumetsat, zoom=0.03125)
        ab = AnnotationBbox(im, (0.887, 0.08), frameon=False, zorder=15, xycoords=ax.transAxes, pad=0)
        ax.add_artist(ab)

        # plt.show()
        plt.savefig(output_plot_directory, dpi=dpi,
                    bbox_inches='tight',
                    pad_inches=0)
