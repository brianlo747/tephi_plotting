import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from radiosonde.load_wyo_upperair import WyomingUpperAirSonde
from radiosonde.calc_wetbulb import wet_bulb_temperature
from plots.radiosonde.skewt.skewt_main import SkewTLogP


def plot_wyoming_skewt(date, station, output_dir, theta_w=False):
    # sonde_obj = WyomingUpperAirSonde(date, station)

    # sonde_data = sonde_obj.get_dataframe()
    # sonde_metadata = sonde_obj.get_metadata()
    # pressures_winds = sonde_obj.prune_data(
    # np.array([1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 300, 250, 200, 100, 50]))

    skt = SkewTLogP()

    pressures = [1008.0, 1001.0, 1000.0]
    skt.plot_profile(pressures,
                     [12.00000, 12.20000, 12.20000],
                     label='Temperature', color='red', linewidth=0.8)
    skt.plot_profile(pressures,
                     [11.00000, 9.50000, 9.60000],
                     label='Dew Point', color='blue', linewidth=0.8)

    # skt.plot_barbs(pressures_winds['pressure'].values, pressures_winds['speed'].values,
    #                pressures_winds['direction'].values + 180.0)
    # skt.plot_main_title(sonde_metadata)
    # skt.read_metadata(sonde_metadata)
    skt.save_tephi(output_dir=output_dir, full_name="failed")
    # skt.save_tephi_manual(output_path=output_dir)
    plt.close('all')


if __name__ == '__main__':

    # Change the following lines
    main_date = datetime(2021, 11, 10, 0)
    station_list = ['03882']
    output_dir = '/Users/brianlo/Desktop/Reading/PhD/WCD/output/panto'
    ############################

    for station_num in station_list:
        try:
            plot_wyoming_skewt(date=main_date,
                               station=station_num,
                               output_dir=output_dir,
                               theta_w=False)
            print(f"Plotted {main_date.strftime('%Y-%m-%d %HZ')} for station {station_num}.")
        except ValueError as ve:
            print(ve)
