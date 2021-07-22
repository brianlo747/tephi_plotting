import numpy as np

from um_global.ukmo_global_model import UkmoGlobalModel
from cmaps.thickness import ThicknessCmap, ThicknessBounds
from cmaps.heights import HeightBounds
from cmaps.temperature import TemperatureCmap, TemperatureBounds
from plots.plot_global_model import GlobalModelPlot

if __name__ == '__main__':
    global_model_obj = UkmoGlobalModel('/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=1000)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=500)
    global_model_obj.calculate_thickness(500, 1000)
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('thickness_1000_500hPa', color_field_cmap=ThicknessCmap.thickness_cmap,
                         color_field_cmap_bounds=ThicknessBounds.thickness_1000_500_bounds,
                         color_field_contours=True,
                         color_field_cbar_labels=np.arange(510, 660, 24),
                         contour_field='geopotential_height_500hPa',
                         contour_field_levels=HeightBounds.height_bounds,
                         plot_title='1000-500 hPa Thickness (dm), 500 hPa Geopotential Height (km)',
                         output_plot_name='test1')

    global_model_obj.read_dataset('wet_bulb_potential_temperature', cell_method='', pressure_level=850)
    global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=300)
    plot_obj = GlobalModelPlot(global_model_obj)
    plot_obj.plot_fields('wet_bulb_potential_temperature_850hPa', color_field_cmap=TemperatureCmap.temperature_cmap,
                         color_field_cmap_bounds=TemperatureBounds.temperature_bounds,
                         color_field_cbar_labels=np.arange(270, 311, 5),
                         contour_field='geopotential_height_300hPa',
                         contour_field_levels=HeightBounds.height_bounds,
                         plot_title='850 hPa Wet-bulb Potential Temperature (K), 300 hPa Geopotential Height (km)',
                         output_plot_name='test2')
