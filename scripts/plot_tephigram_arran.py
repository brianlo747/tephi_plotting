import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from radiosonde.load_wyo_upperair import WyomingUpperAirSonde
from radiosonde.calc_wetbulb import wet_bulb_temperature
from plots.radiosonde.tephigram.tephigram_main import Tephigram


def plot_wyoming_tephigram(date, station, theta_w=False):
    sonde_obj = WyomingUpperAirSonde(date, station)

    sonde_data = sonde_obj.get_dataframe()
    sonde_metadata = sonde_obj.get_metadata()
    pressures_winds = sonde_obj.prune_data(
        np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 300, 250, 200, 100, 50]))

    tpg = Tephigram()

    tpg.plot_profile(sonde_data['pressure'].values, sonde_data['temperature'].values,
                     label='Temperature', color='red', linewidth=0.8)
    tpg.plot_profile(sonde_data['pressure'].values, sonde_data['dewpoint'].values,
                     label='Dew Point', color='blue', linewidth=0.8)
    if theta_w:
        wet_bulb = wet_bulb_temperature(sonde_data['pressure'].values * 100,
                                        sonde_data['temperature'].values + 273.15,
                                        sonde_data['dewpoint'].values + 273.15)
        tpg.plot_profile(sonde_data['pressure'].values, wet_bulb - 273.15,
                         label='Wet Bulb', color='violet', linewidth=0.8)

    tpg.plot_barbs(pressures_winds['pressure'].values, pressures_winds['speed'].values,
                   pressures_winds['direction'].values + 180.0)
    tpg.plot_main_title(sonde_metadata)
    tpg.read_metadata(sonde_metadata)
    tpg.save_tephi(output_dir='/Users/brianlo/Desktop/Reading/PhD/WCD/output/tephis_arran/')  # Change output dir!!
    # plt.show()
    plt.close('all')


if __name__ == '__main__':
    main_date = datetime(2021, 9, 20, 0)
    station_list = ['03005', '03023', '03238', '03354', '03502', '03590',
                    '03693', '03743', '03808', '03882', '03918', '03953']
    for station_num in station_list:
        try:
            plot_wyoming_tephigram(date=main_date, station=station_num, theta_w=False)
            print(f"Plotted {main_date.strftime('%Y-%m-%d %HZ')} for station {station_num}.")
        except ValueError as ve:
            print(ve)
