import numpy as np
import matplotlib.pyplot as plt
from radiosonde.load_spf import RadiosondeMetDB
from radiosonde.calc_wetbulb import wet_bulb_temperature
from plots.radiosonde.tephigram.tephigram_main import Tephigram


def plot_all_tephigrams(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_23Z20210726'):
    sonde_obj = RadiosondeMetDB(infile)
    for i in range(sonde_obj.max_observations):
        metadata, pressures_temperatures = sonde_obj.get_datacols_no_na(i + 1, ['PnPn', 'TnTnTn'])
        _, pressures_temperatures_dews = sonde_obj.get_datacols_no_na(i + 1, ['PnPn', 'TnTnTn', 'DnDn'])
        _, pressures_dews = sonde_obj.get_datacols_no_na(i + 1, ['PnPn', 'DnDn'])
        _, pressures_winds = sonde_obj.get_datacols_no_na(i + 1, ['PnPn', 'dndn', 'fnfnfn'])
        pressures_winds = sonde_obj.prune_data(
            np.array(
                [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 100, 50]) * 100,
            pressures_winds)

        # Calculate Tw
        wet_bulb = wet_bulb_temperature(pressures_temperatures_dews['PnPn'].values,
                                        pressures_temperatures_dews['TnTnTn'].values,
                                        pressures_temperatures_dews['DnDn'].values)

        tpg = Tephigram()

        tpg.plot_profile(pressures_temperatures['PnPn'] / 100, pressures_temperatures['TnTnTn'] - 273.15,
                         label='Temperature', color='red', linewidth=0.8)
        tpg.plot_profile(pressures_dews['PnPn'] / 100, pressures_dews['DnDn'] - 273.15,
                         label='Dew Point', color='blue', linewidth=0.8)
        tpg.plot_profile(pressures_temperatures['PnPn'] / 100, wet_bulb - 273.15,
                         label='Wet Bulb', color='violet', linewidth=0.8)
        tpg.plot_barbs(pressures_winds['PnPn'] / 100, pressures_winds['fnfnfn'] * 1.94384449,
                       pressures_winds['dndn'] + 180.0)
        tpg.plot_main_title(metadata)
        tpg.read_metadata(metadata)
        tpg.save_tephi(output_dir='/Users/brianlo/Desktop/Reading/PhD/WCD/output/tephis/')
        plt.close('all')


if __name__ == '__main__':
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_05Z20210726')
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_23Z20210726')
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_11Z20210726')
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_09Z20210726')
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_23Z20210101')
    plot_all_tephigrams('/Users/brianlo/Desktop/Reading/PhD/WCD/data/Temps_11Z20210101')
