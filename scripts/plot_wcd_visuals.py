import numpy as np

from um_global.ukmo_global_model import UkmoGlobalModel
from cmaps.thickness import ThicknessCmap, ThicknessBounds
from cmaps.heights import HeightBounds
from cmaps.temperature import TemperatureCmap, TemperatureBounds
from cmaps.precip import PrecipCmap, PrecipBounds
from cmaps.pressure import PressureBounds
from plots.plot_global_model import GlobalModelPlot


def plot1():
    global_model_obj = UkmoGlobalModel('/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
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
                         contour_field='geopotential_height_500hPa',
                         contour_field_levels=HeightBounds.height_bounds,
                         plot_title='1000-500 hPa Thickness (dam), 500 hPa Geopotential Height (km)',
                         output_plot_name='test1')


def plot2():
    global_model_obj = UkmoGlobalModel('/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    global_model_obj.read_dataset('wet_bulb_potential_temperature', cell_method='', pressure_level=850)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=300)
    global_model_obj.convert_units('geopotential_height_300hPa', new_units='km')
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('wet_bulb_potential_temperature_850hPa', color_field_cmap=TemperatureCmap.temperature_cmap,
                         color_field_cmap_bounds=TemperatureBounds.temperature_bounds,
                         color_field_cbar_labels=np.arange(270, 311, 5),
                         contour_field='geopotential_height_300hPa',
                         contour_field_levels=HeightBounds.height_bounds,
                         plot_title='850 hPa Wet-bulb Potential Temperature (K), 300 hPa Geopotential Height (km)',
                         output_plot_name='test2')


def plot3():
    global_model_obj = UkmoGlobalModel('/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
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
                         contour_field='air_pressure_at_sea_level',
                         contour_field_levels=PressureBounds.mslp_bounds,
                         contour_field2='thickness_1000_500hPa',
                         contour_field2_levels=ThicknessBounds.thickness_1000_500_bounds,
                         plot_title='Total Rain Rate (mm/hr), MSLP (hPa), 1000-500 hPa Thickness (dam)',
                         output_plot_name='test3')


if __name__ == '__main__':
    # plot1()
    # plot2()
    plot3()
