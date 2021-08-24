import numpy as np

from sat.load_autosat import AutoSat
from um_global.ukmo_global_model import UkmoGlobalModel
from cmaps.thickness import ThicknessCmap, ThicknessBounds
from cmaps.heights import HeightBounds
from cmaps.temperature import TemperatureCmap, TemperatureBounds
from cmaps.precip import PrecipCmap, PrecipBounds
from cmaps.pressure import PressureBounds
from plots.plot_global_model import GlobalModelPlot
from plots.plot_sat import SatPlot


def plot1(infile):
    global_model_obj = UkmoGlobalModel(infile)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=1000)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=500)
    global_model_obj.calculate_thickness(500, 1000)
    global_model_obj.convert_units('thickness_1000_500hPa', new_units='dam')
    global_model_obj.convert_units('geopotential_height_500hPa', new_units='km')
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('thickness_1000_500hPa', color_field_cmap=ThicknessCmap.thickness_cmap,
                         color_field_cmap_bounds=ThicknessBounds.thickness_1000_500_bounds,
                         color_field_contours=True,
                         color_field_cbar_labels=np.arange(510, 660, 24),
                         contour_field1='geopotential_height_500hPa',
                         contour_field1_levels=HeightBounds.height_bounds,
                         plot_title='1000-500 hPa Thickness (dam), 500 hPa Geopotential Height (km)',
                         output_plot_directory=
                         f'/Users/brianlo/Desktop/Reading/PhD/WCD/output/global/thickness_{infile[-18:-3]}.png')


def plot2(infile):
    global_model_obj = UkmoGlobalModel(infile)
    global_model_obj.read_dataset('wet_bulb_potential_temperature', cell_method='', pressure_level=850)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=300)
    global_model_obj.convert_units('geopotential_height_300hPa', new_units='km')
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('wet_bulb_potential_temperature_850hPa', color_field_cmap=TemperatureCmap.temperature_cmap,
                         color_field_cmap_bounds=TemperatureBounds.temperature_bounds,
                         color_field_cbar_labels=np.arange(270, 311, 5),
                         contour_field1='geopotential_height_300hPa',
                         contour_field1_levels=HeightBounds.height_bounds,
                         plot_title='850 hPa Wet-bulb Potential Temperature (K), 300 hPa Geopotential Height (km)',
                         output_plot_directory=
                         f'/Users/brianlo/Desktop/Reading/PhD/WCD/output/global/wet_bulb_{infile[-18:-3]}.png')


def plot3(infile):
    global_model_obj = UkmoGlobalModel(infile)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=1000)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=500)
    global_model_obj.calculate_thickness(500, 1000)
    global_model_obj.convert_units('thickness_1000_500hPa', new_units='dam')
    global_model_obj.read_dataset('air_pressure_at_sea_level', cell_method='')
    global_model_obj.read_dataset('convective_rainfall_flux', cell_method='')
    global_model_obj.read_dataset('stratiform_rainfall_flux', cell_method='')
    global_model_obj.convert_units('air_pressure_at_sea_level', new_units='hPa')
    global_model_obj.calculate_total_rainfall_rate()
    global_model_obj.convert_units('total_rainfall_rate', new_units='kg m-2 hr-1')
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('total_rainfall_rate', color_field_cmap=PrecipCmap.precip_cmap,
                         color_field_cmap_bounds=PrecipBounds.precip_rate_bounds_with_ex,
                         color_field_cbar_labels=PrecipBounds.precip_rate_bounds,
                         contour_field1='air_pressure_at_sea_level',
                         contour_field1_levels=PressureBounds.mslp_bounds,
                         contour_field2='thickness_1000_500hPa',
                         contour_field2_levels=ThicknessBounds.thickness_1000_500_bounds,
                         plot_title='Total Rain Rate (mm/hr), MSLP (hPa), 1000-500 hPa Thickness (dam)',
                         output_plot_directory=
                         f'/Users/brianlo/Desktop/Reading/PhD/WCD/output/global/rainrate_{infile[-18:-3]}.png')


def plot4(infile_sat, infile_model):
    sat_obj = AutoSat(infile_sat)
    global_model_obj = UkmoGlobalModel(infile_model)
    global_model_obj.read_dataset('air_pressure_at_sea_level', cell_method='')
    global_model_obj.convert_units('air_pressure_at_sea_level', new_units='hPa')
    plot_obj = SatPlot(sat_obj, global_model_obj)
    plot_obj.plot_fields(contour_field1='air_pressure_at_sea_level',
                         contour_field1_levels=PressureBounds.mslp_bounds,
                         plot_title='MSLP (hPa)',
                         output_plot_directory=
                         f'/Users/brianlo/Desktop/Reading/PhD/WCD/output/global/sat_{infile_model[-18:-3]}.png')


if __name__ == '__main__':
    plot1(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    plot2(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    plot3(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    plot4(infile_sat='/Users/brianlo/Desktop/Reading/PhD/WCD/data/eieu502107090100.dat',
          infile_model='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_012.pp')
    plot1(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_012.pp')
    plot2(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_012.pp')
    plot3(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_012.pp')
