import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pyproj
import cartopy
import cartopy.crs as ccrs
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sat.load_autosat import AutoSat

if __name__ == '__main__':
    autosat_obj = AutoSat(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/eieu502107090100.dat')
    plt.figure(figsize=(14, 10))
    prj = ccrs.Stereographic(
        true_scale_latitude=60,
        central_longitude=-35,
        central_latitude=90)
    ax = plt.axes(projection=prj)
    plt.subplots_adjust(left=0, bottom=0, right=1.0, top=1.0, wspace=None, hspace=None)
    ax.axis('off')

    # Projection string:
    # "+proj=stere +ellps=WGS84 +lat_0=90 +lon_0=-35 +x_0=0 +y_0=0 +lat_ts=60 +no_defs"
    transform_latlon_to_stere = pyproj.Transformer.from_proj('epsg:4326', prj.proj4_init, always_xy=True)
    bl_x, bl_y = transform_latlon_to_stere.transform(autosat_obj.bl_long / 1000, autosat_obj.bl_lat / 1000)
    tr_x, tr_y = transform_latlon_to_stere.transform(autosat_obj.tr_long / 1000, autosat_obj.tr_lat / 1000)

    lat_lines = np.arange(20, 85, 10)
    lon_lines = np.arange(-80, 100, 10)
    ax.coastlines(resolution='50m', color='white', linewidth=0.5)
    bodr = cartopy.feature.NaturalEarthFeature(category='cultural',
                                               name='admin_0_boundary_lines_land', scale='50m', facecolor='none',
                                               alpha=0.7)
    ax.add_feature(bodr, edgecolor='white', linewidth=0.5)
    gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5)
    gl.xlocator = mticker.FixedLocator(lon_lines)
    gl.ylocator = mticker.FixedLocator(lat_lines)

    img_extent = (bl_x, tr_x, bl_y, tr_y)
    # img_extent = (-53.927, 46.778, 10.247, 33.422)
    img = autosat_obj.sat_image
    ax.imshow(img, origin='lower', extent=img_extent, transform=prj, cmap='gist_yarg',
              vmin=0, vmax=255, zorder=-1)
    # coords = prj.transform_points(
    #     ccrs.PlateCarree(), np.asarray([-53.9666666667, 49.7333333333]), np.asarray([34.7166666667, 37.1166666667]))
    coords = prj.transform_points(
        ccrs.PlateCarree(), np.asarray([-53.927, 46.778]), np.asarray([32.247, 33.422]))
    ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], prj)
    # ax.set_extent((-60, 40, 20, 70), crs=ccrs.PlateCarree())

    # Black rectangle at bottom
    ax.add_patch(Rectangle((0, 0.9), 0.2, 0.1, alpha=1, zorder=15, transform=ax.transAxes,
                           facecolor='black'))
    obs_dt_string = f"{autosat_obj.obs_time_year:04}-{autosat_obj.obs_time_month:02}-{autosat_obj.obs_time_day:02} " \
                    f"{autosat_obj.obs_time_hour:02}:{autosat_obj.obs_time_minute:02}:{autosat_obj.obs_time_second:02}Z"
    ax.text(0.005, 0.975, "Meteosat 0° IR 10.8",
            horizontalalignment='left',
            verticalalignment='center',
            color='white', zorder=16,
            size=16, transform=ax.transAxes)
    ax.text(0.005, 0.925, obs_dt_string,
            horizontalalignment='left',
            verticalalignment='center',
            color='white', zorder=16,
            size=16, transform=ax.transAxes)

    # Logo
    logo_ukmo = plt.imread('/Users/brianlo/Desktop/Reading/PhD/WCD/data/1200px-Met_Office_white.svg.png')
    im = OffsetImage(logo_ukmo, zoom=0.05)
    ab = AnnotationBbox(im, (0.96, 0.06), frameon=False, zorder=15, xycoords=ax.transAxes, pad=0)
    ax.add_artist(ab)

    logo_eumetsat = plt.imread('/Users/brianlo/Desktop/Reading/PhD/WCD/data/1280px-EUMETSAT_logo_white.svg.png')
    im = OffsetImage(logo_eumetsat, zoom=0.0625)
    ab = AnnotationBbox(im, (0.885, 0.06), frameon=False, zorder=15, xycoords=ax.transAxes, pad=0)
    ax.add_artist(ab)

    plt.savefig('ir_sat.png', dpi=300, bbox_inches='tight',
                pad_inches=0)
