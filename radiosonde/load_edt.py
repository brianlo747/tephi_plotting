import os
import pandas as pd

from radiosonde.calc_wetbulb import dewpoint, saturation_vapor_pressure


class WesconRadiosonde(object):
    def __init__(self, infile):
        self.filename = os.path.split(infile)[1]

        lines_to_end = 0
        # Radiosonde data
        with open(infile, encoding="ISO-8859-1") as edt_file:
            for num, line in enumerate(edt_file, 1):
                if 'Radiosonde data' in line:
                    lines_to_skip = num
                if line == '\n':
                    lines_to_end = num - 1
                    break
        self.df_rad = pd.read_csv(infile, sep='\t', skiprows=lines_to_skip, nrows=lines_to_end - lines_to_skip,
                                  header=None, index_col=0,
                                  encoding="ISO-8859-1")
        self.df_rad.index = self.df_rad.index.str.lstrip()
        self.df_rad.index = self.df_rad.index.str.rstrip()

        # Release data
        with open(infile, encoding="ISO-8859-1") as edt_file:
            for num, line in enumerate(edt_file, 1):
                if num <= lines_to_end + 1:
                    continue
                if 'Release data' in line:
                    lines_to_skip = num
                if line == '\n':
                    lines_to_end = num - 1
                    break
        self.df_red = pd.read_csv(infile, sep='\t', skiprows=lines_to_skip, nrows=lines_to_end - lines_to_skip,
                                  skip_blank_lines=False,
                                  header=None, index_col=0,
                                  encoding="ISO-8859-1")
        self.df_red.index = self.df_red.index.str.lstrip()
        self.df_red.index = self.df_red.index.str.rstrip()
        self.df_red = self.df_red[self.df_red.index != '']

        # Surface data
        with open(infile, encoding="ISO-8859-1") as edt_file:
            for num, line in enumerate(edt_file, 1):
                if num <= lines_to_end + 1:
                    continue
                if 'Surface data' in line:
                    lines_to_skip = num
                if line == '\n':
                    lines_to_end = num - 1
                    break
        self.df_sud = pd.read_csv(infile, sep='\t', skiprows=lines_to_skip, nrows=lines_to_end - lines_to_skip,
                                  header=None, index_col=0,
                                  encoding="ISO-8859-1")
        self.df_sud.index = self.df_sud.index.str.lstrip()
        self.df_sud.index = self.df_sud.index.str.rstrip()

        # Calibration data
        with open(infile, encoding="ISO-8859-1") as edt_file:
            for num, line in enumerate(edt_file, 1):
                if num <= lines_to_end + 1:
                    continue
                if 'Calibration data' in line:
                    lines_to_skip = num
                if line == '\n':
                    lines_to_end = num - 1
                    break
        self.df_cad = pd.read_csv(infile, sep='\t', skiprows=lines_to_skip, nrows=lines_to_end - lines_to_skip,
                                  header=None, index_col=0,
                                  encoding="ISO-8859-1")
        self.df_cad.index = self.df_cad.index.str.lstrip()
        self.df_cad.index = self.df_cad.index.str.rstrip()

        # Line header lookup
        lookup = 'TimeUTC'

        lines_to_skip = 0
        with open(infile, encoding="ISO-8859-1") as edt_file:
            for num, line in enumerate(edt_file, 1):
                if lookup in line:
                    lines_to_skip = num - 1
                    break

        self.df = pd.read_csv(infile, sep='\t', skiprows=lines_to_skip, encoding="ISO-8859-1",
                              skipinitialspace=True).drop([0])
        self.df.columns = self.df.columns.str.lstrip()
        data_col_names = ["P", "Temp", "RH", "Dewp", "Speed", "Dir", "Ecomp", "Ncomp", "Lat", "Lon", "AscRate",
                          "HeightMSL", "GpsHeightMSL", "PotTemp", "SpHum", "CompRng", "CompAz", "VirT", "SatVapP",
                          "VapP", "MixR", "Den", "HeightGnd", "GpsHeightGnd", "HeightE", "Pm", "Pc", "Ddep", "PEPT",
                          "SSpc", "RI", "MRI", "RIG", "ELR"]
        self.df[data_col_names] = self.df[data_col_names].apply(pd.to_numeric, errors='coerce')
        self.df.rename(columns={"P": "Pressure",
                                "Temp": "Temperature",
                                "Dewp": "Dewpoint",
                                "Speed": "WindSpeed",
                                "Dir": "WindDir"},
                       inplace=True)
        self.sonde_model = None
        self.location = None
        self.date_str = None
        self.time_str = None

    def get_metadata(self):
        # long_filename = self.filename
        # if self.filename[-4:] == ".txt":
        #     long_filename = self.filename[:-4]
        # filename_segments = long_filename.split("_", 3)
        # self.sonde_model = filename_segments[0]
        # self.location = filename_segments[1]
        # self.date_str = filename_segments[2]
        # self.time_str = filename_segments[3]

        self.location = self.df_red.loc["Station name", 1]
        self.date_str = self.df_red.loc["Balloon release date and time", 1]

        meta_df = pd.DataFrame(
            {'field': ['LOCATION', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINT'],
             'info': [self.location,
                      int(self.date_str[0:4]),
                      int(self.date_str[5:7]),
                      int(self.date_str[8:10]),
                      int(self.date_str[11:13]),
                      int(self.date_str[14:16])
                      ]})
        meta_df = meta_df.set_index('field')
        return meta_df

    def prune_data(self, prune_pressure_list):
        # Collect rows as DataFrames instead of Series to preserve dtypes
        rows = []
        for prune_pressure in prune_pressure_list:
            idx = (self.df['Pressure'] - prune_pressure).abs().idxmin()
            rows.append(self.df.iloc[[idx]])  # Note the double brackets → keeps it as DataFrame

        # Concatenate vertically, preserving dtypes
        pruned_profile = pd.concat(rows, ignore_index=True)

        # Drop duplicates properly
        pruned_profile = pruned_profile.drop_duplicates(subset=['Pressure'])

        return pruned_profile


if __name__ == '__main__':
    sonde = WesconRadiosonde("/Users/brianlo/Downloads/edt1sdataforv217_20230612_1402.txt")
    pass
