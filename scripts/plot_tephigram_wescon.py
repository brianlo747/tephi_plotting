import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from radiosonde.load_edt import WesconRadiosonde
from radiosonde.calc_wetbulb import wet_bulb_temperature
from plots.radiosonde.tephigram.tephigram_main import Tephigram


def plot_wescon_tephigram(infile, outpath, outfile=None, theta_w=False):
    sonde_obj = WesconRadiosonde(infile)
    sonde_data = sonde_obj.df
    sonde_metadata = sonde_obj.get_metadata()
    pressures_winds = sonde_obj.prune_data(
        np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50]))

    tpg = Tephigram()

    tpg.plot_profile(sonde_data['Pressure'].values, sonde_data['Temperature'].values,
                     label='Temperature', color='red', linewidth=0.8)
    tpg.plot_profile(sonde_data['Pressure'].values, sonde_data['Dewpoint'].values,
                     label='Dew Point', color='blue', linewidth=0.8)
    if theta_w:
        wet_bulb = wet_bulb_temperature(sonde_data['Pressure'].values * 100,
                                        sonde_data['Temperature'].values + 273.15,
                                        sonde_data['Dewpoint'].values + 273.15)
        tpg.plot_profile(sonde_data['Pressure'].values, wet_bulb - 273.15,
                         label='Wet Bulb', color='violet', linewidth=0.8)

    tpg.plot_barbs(pressures_winds['Pressure'].values, pressures_winds['WindSpeed'].values * 1.94384,
                   pressures_winds['WindDir'].values + 180)
    tpg.plot_dorset_title(sonde_metadata)
    tpg.read_metadata_dorset(sonde_metadata)
    if outfile is not None:
        tpg.save_tephi_manual(output_path=f"{outfile}.png", dpi=300)
        tpg.save_tephi_manual(output_path=f"{outfile}.pdf")
    else:
        output_name = f"{sonde_metadata.loc['LOCATION', 'info']}_" \
                      f"{str(sonde_metadata.loc['YEAR', 'info']).zfill(2)}" \
                      f"{str(sonde_metadata.loc['MONTH', 'info']).zfill(2)}" \
                      f"{str(sonde_metadata.loc['DAY', 'info']).zfill(2)}_" \
                      f"{str(sonde_metadata.loc['HOUR', 'info']).zfill(2)}" \
                      f"{str(sonde_metadata.loc['MINT', 'info']).zfill(2)}"
        tpg.save_tephi_manual(output_path=os.path.join(outpath, f"{output_name}.png"), dpi=300)
        tpg.save_tephi_manual(output_path=os.path.join(outpath, f"{output_name}.pdf"))
    plt.close('all')


if __name__ == '__main__':
    # Change the following lines
    files = glob.glob("/Users/brianlo/Desktop/Reading/PhD/WESCON/sonde_data/20230621/*")
    for input_file in files:
        # input_file = '/Users/brianlo/Downloads/edt1sdataforv217_20230612_1402.txt'
        # output_file = '/Users/brianlo/Desktop/Reading/PhD/WCD/output/tephis_wescon/test1'
        ############################
        plot_wescon_tephigram(infile=input_file,
                              outpath="/Users/brianlo/Desktop/Reading/PhD/WCD/output/tephis_wescon",
                              theta_w=True)
        print(f"Plotted {input_file}.")
