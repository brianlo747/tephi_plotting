import numpy as np
import matplotlib.pyplot as plt
from radiosonde.load_csv import DorsetRadiosonde
from radiosonde.calc_wetbulb import wet_bulb_temperature
from plots.radiosonde.tephigram.tephigram_main import Tephigram


def plot_dorset_tephigram(infile, outfile, theta_w=False):
    sonde_obj = DorsetRadiosonde(infile)
    sonde_obj.calc_dewpoint()
    sonde_data = sonde_obj.df
    sonde_metadata = sonde_obj.get_metadata()
    pressures_winds = sonde_obj.prune_data(
        np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50]))

    tpg = Tephigram()

    tpg.plot_profile(sonde_data['Pressure'].values, sonde_data['Temperature'].values - 273.15,
                     label='Temperature', color='red', linewidth=0.8)
    tpg.plot_profile(sonde_data['Pressure'].values, sonde_data['Dewpoint'].values,
                     label='Dew Point', color='blue', linewidth=0.8)
    if theta_w:
        wet_bulb = wet_bulb_temperature(sonde_data['Pressure'].values * 100,
                                        sonde_data['Temperature'].values,
                                        sonde_data['Dewpoint'].values + 273.15)
        tpg.plot_profile(sonde_data['Pressure'].values, wet_bulb - 273.15,
                         label='Wet Bulb', color='violet', linewidth=0.8)

    tpg.plot_barbs(pressures_winds['Pressure'].values, pressures_winds['WindSpeed'].values * 1.94384,
                   pressures_winds['WindDir'].values + 180)
    tpg.plot_dorset_title(sonde_metadata)
    tpg.read_metadata_dorset(sonde_metadata)
    tpg.save_tephi_manual(output_path=f"{outfile}.png", dpi=300)
    tpg.save_tephi_manual(output_path=f"{outfile}.pdf")
    plt.close('all')


if __name__ == '__main__':
    # Change the following lines
    input_file = '/Users/brianlo/Downloads/MW41-Reading-20250322-122409-SynchronizedSoundingData.csv'
    output_file = '/Users/brianlo/Downloads/MW41-Reading-20250322-122409-SynchronizedSoundingData.png'
    ############################
    plot_dorset_tephigram(infile=input_file,
                          outfile=output_file,
                          theta_w=True, # Set to False for your students to
                                        # draw the wet-bulb potential temperature line on their own 😈
                          )
    print(f"Plotted {input_file} and saved to {output_file}")
