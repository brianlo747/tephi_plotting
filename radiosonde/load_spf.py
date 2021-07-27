import sys
import array
import numpy as np
import pandas as pd


class Radiosonde(object):

    def __init__(self, infile):
        if infile.endswith('.spf'):
            self._from_raw(infile)
        elif infile.endswith('.edt'):
            self._from_raw(infile)
        elif infile.endswith('.tsv'):
            self._from_tsv(infile)

    def _from_raw(self, infile):
        with open(infile, "rb") as f:
            data = f.read()
        f.close()

        # Check system endianness
        endianness = sys.byteorder

        header = data[0:50]
        ident = data[50:246]
        syspar = data[246:8333]
        sounding = data[8333:]

        tab_1_header = array.array("B")
        tab_1_header.frombytes(header[0:20])
        self.file_header = tab_1_header.tobytes()

        tab_1_ints = array.array("H")
        tab_1_ints.frombytes(header[20:32])
        if endianness == 'big':
            tab_1_ints.byteswap()
        self.length_of_identification_block_in_bytes = tab_1_ints[0]
        self.length_of_syspar_in_bytes = tab_1_ints[1]
        self.number_of_data_records = tab_1_ints[2]
        self.number_of_standard_levels = tab_1_ints[3]
        self.type_of_data = tab_1_ints[4]
        self.length_of_data_record_in_bytes = tab_1_ints[5]

        tab_1_bytes = array.array("B")
        tab_1_bytes.frombytes(header[32:33])
        if endianness == 'big':
            tab_1_bytes.byteswap()
        self.file_ready_flag = tab_1_bytes[0]

        tab_2_ints = array.array("H")
        tab_2_ints.frombytes(
            ident[0:28] + ident[32:52] + ident[70:80] + ident[100:158] + ident[159:165] + ident[166:196])
        if endianness == 'big':
            tab_2_ints.byteswap()
        self.station_type = tab_2_ints[0]
        self.region_number = tab_2_ints[1]
        self.wmo_block_number = tab_2_ints[2]
        self.wmo_station_number = tab_2_ints[3]
        self.station_latitude = tab_2_ints[4] * 0.01
        self.station_longitude = tab_2_ints[5] * 0.01
        self.station_altitude = tab_2_ints[6]
        self.wind_speed_unit_in_message = tab_2_ints[7]
        self.use_of_telecommunication_headings = tab_2_ints[8]
        self.res = tab_2_ints[9]
        self.sounding_type = tab_2_ints[10]
        self.start_mode = tab_2_ints[11]
        self.time_elapsed_at_the_start_of_ascent = tab_2_ints[12]
        self.ptu_rate = tab_2_ints[13]
        self.year = tab_2_ints[14]
        self.month = tab_2_ints[15]
        self.day = tab_2_ints[16]
        self.julian_date = tab_2_ints[17]
        self.hour = tab_2_ints[18]
        self.minute = tab_2_ints[19]
        self.message_year = tab_2_ints[20]
        self.message_month = tab_2_ints[21]
        self.message_day = tab_2_ints[22]
        self.message_hour = tab_2_ints[23]
        self.surface_pressure = tab_2_ints[24]
        self.surface_temperature = tab_2_ints[25]
        self.surface_humidity = tab_2_ints[26]
        self.surface_wind_direction = tab_2_ints[27]
        self.surface_wind_speed = tab_2_ints[28]
        self.pressure_correction = tab_2_ints[29]
        self.temperature_correction = tab_2_ints[30]
        self.humidity_correction = tab_2_ints[31]
        self.succ_of_signal = tab_2_ints[32]
        self.pressure_accept_level = tab_2_ints[33]
        self.pressure_replace_level = tab_2_ints[34]
        self.pressure_reject_level = tab_2_ints[35]
        self.temperature_accept_level = tab_2_ints[36]
        self.temperature_replace_level = tab_2_ints[37]
        self.temperature_reject_level = tab_2_ints[38]
        self.humidity_accept_level = tab_2_ints[39]
        self.humidity_replace_level = tab_2_ints[40]
        self.humidity_reject_level = tab_2_ints[41]
        self.total_omega_count = tab_2_ints[42]
        self.reason_of_termination = tab_2_ints[43]
        self.omega_count = tab_2_ints[44:55]
        self.wind_computing_mode = tab_2_ints[55]
        self.wind_mode = tab_2_ints[56]
        self.loran_omega_stations_used = tab_2_ints[57]
        self.gri_of_chain_1 = tab_2_ints[58]
        self.gri_of_chain_2 = tab_2_ints[59]
        self.excluded_loran_c_transmitters = tab_2_ints[60]
        self.phase_integration_time_1 = tab_2_ints[61]
        self.phase_integration_time_2 = tab_2_ints[62]
        self.phase_integration_time_3 = tab_2_ints[63]
        self.phase_integration_time_4 = tab_2_ints[64]
        self.phase_integration_time_5 = tab_2_ints[65]
        self.phase_integration_time_6 = tab_2_ints[66]
        self.phase_integration_change_level_1 = tab_2_ints[67]
        self.phase_integration_change_level_2 = tab_2_ints[68]
        self.phase_integration_change_level_3 = tab_2_ints[69]
        self.phase_integration_change_level_4 = tab_2_ints[70]
        self.phase_integration_change_level_5 = tab_2_ints[71]
        self.phase_integration_change_level_6 = tab_2_ints[72]
        self.reference_pressure = tab_2_ints[73]
        self.reference_temperature = tab_2_ints[74]
        self.reference_humidity = tab_2_ints[75]

        tab_2_longs = array.array("H")
        tab_2_longs.frombytes(ident[28:32])
        if endianness == 'big':
            tab_2_longs.byteswap()
        self.spu_card_serial_number = tab_2_longs[0]

        tab_2_bytes = array.array("B")
        tab_2_bytes.frombytes(ident[52:70] + ident[80:100] + ident[158:159] + ident[165:166])
        if endianness == 'big':
            tab_2_bytes.byteswap()
        self.cloud_group = tab_2_bytes[0:6]
        self.weather_group = tab_2_bytes[6:12]
        self.napp = tab_2_bytes[12:18]
        self.radiosonde_number = tab_2_bytes[18:28]
        self.sounding_number = tab_2_bytes[28:38]
        self.number_of_loran_c_chains_in_use = tab_2_bytes[38]
        self.unit_to_control_change_of_phase_integration_time = tab_2_bytes[39]

        df_obj = pd.DataFrame(columns=['elapsed_time_since_sonde_release',
                                       'scaled_logarithmic_pressure',
                                       'temperature',
                                       'humidity',
                                       'north_component_of_wind',
                                       'east_component_of_wind',
                                       'altitude_above_mean_sea_level',
                                       'pressure',
                                       'dew_point_temperature',
                                       'mixing_ratio',
                                       'wind_direction',
                                       'wind_speed',
                                       'azimuth_to_the_sonde',
                                       'horizontal_distance_to_the_sonde',
                                       'sonde_position_longitude',
                                       'sonde_position_latitude',
                                       'sond_calculated_significance_key',
                                       'used_edited_recalculated_significance_key',
                                       'radar_height'])

        for idx in range(self.number_of_data_records + 25):
            row_pos = self.length_of_data_record_in_bytes * idx
            data_floats = array.array("f")
            data_floats.frombytes(sounding[row_pos + 0:row_pos + 4])
            data_ints = array.array("H")
            data_ints.frombytes(sounding[row_pos + 4:row_pos + 40])
            if endianness == 'big':
                data_floats.byteswap()
                data_ints.byteswap()

            row_dict = {'elapsed_time_since_sonde_release': data_floats[0],
                        'scaled_logarithmic_pressure': data_ints[0] / 4096,
                        'temperature': data_ints[1] * 0.1,
                        'humidity': data_ints[2],
                        'north_component_of_wind': data_ints[3] * 0.01,
                        'east_component_of_wind': data_ints[4] * 0.01,
                        'altitude_above_mean_sea_level': data_ints[5],
                        'pressure': data_ints[6] * 0.1,
                        'dew_point_temperature': data_ints[7] * 0.1,
                        'mixing_ratio': data_ints[8] * 0.1,
                        'wind_direction': data_ints[9],
                        'wind_speed': data_ints[10] * 0.1,
                        'azimuth_to_the_sonde': data_ints[11],
                        'horizontal_distance_to_the_sonde': data_ints[12] * 100,
                        'sonde_position_longitude': data_ints[13] * 0.01,
                        'sonde_position_latitude': data_ints[14] * 0.01,
                        'sond_calculated_significance_key': data_ints[15],
                        'used_edited_recalculated_significance_key': data_ints[16],
                        'radar_height': data_ints[17]}
            df_obj = df_obj.append(row_dict, ignore_index=True)

        self.sounding_data = df_obj

    def _from_tsv(self, infile):
        col_names = ['elapsed_time_since_sonde_release',
                     'scaled_logarithmic_pressure',
                     'temperature',
                     'humidity',
                     'north_component_of_wind',
                     'east_component_of_wind',
                     'altitude_above_mean_sea_level',
                     'pressure',
                     'dew_point_temperature',
                     'mixing_ratio',
                     'wind_direction',
                     'wind_speed',
                     'azimuth_to_the_sonde',
                     'horizontal_distance_to_the_sonde',
                     'sonde_position_longitude',
                     'sonde_position_latitude',
                     'sond_calculated_significance_key',
                     'used_edited_recalculated_significance_key',
                     'radar_height']
        df_obj = pd.read_csv(infile, sep='\t', header=1, names=col_names, skiprows=42, index_col=False)
        df_obj['scaled_logarithmic_pressure'] = df_obj['scaled_logarithmic_pressure'] / 4096
        df_obj.replace({-32768: np.nan}, inplace=True)
        self.sounding_data = df_obj
        print(self.sounding_data)


if __name__ == '__main__':
    # Radiosonde(
    #     infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/metoffice-radiosonde_herstmonceux_20200901231505.spf')
    # Radiosonde(
    #     infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/metoffice-radiosonde_herstmonceux_20200720231505.spf')
    Radiosonde(
        infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/metoffice-vaisala-rs41-sg-radiosonde_herstmonceux_20200720231505_autosonde-launch.tsv')
