import pandas as pd
from datetime import datetime
from siphon.simplewebservice.wyoming import WyomingUpperAir


class WyomingUpperAirSonde(object):
    def __init__(self, date, station):
        self.df = WyomingUpperAir.request_data(date, station)
        self.df.dropna(inplace=True)
        # print(self.df)

    def get_dataframe(self):
        return self.df

    def get_metadata(self):
        meta_df = pd.DataFrame(
            {'field': ['WMO_BLCK_NMBR', 'WMO_STTN_NMBR', 'RPRT_IDNY', 'LTTD', 'LNGD', 'YEAR', 'MONTH', 'DAY', 'HOUR',
                       'MINT', 'STTN_HGHT', 'PESR_SNSR_HGHT', 'RPRT_TEXT', 'LEVL_RPLTN_CONT'],
             'info': [int(str(self.df['station_number'].iloc[0]).zfill(5)[0:2]),
                      int(str(self.df['station_number'].iloc[0]).zfill(5)[2:5]),
                      None,
                      self.df['latitude'].iloc[0],
                      self.df['longitude'].iloc[0],
                      self.df['time'].iloc[0].year,
                      self.df['time'].iloc[0].month,
                      self.df['time'].iloc[0].day,
                      self.df['time'].iloc[0].hour,
                      self.df['time'].iloc[0].minute,
                      self.df['elevation'].iloc[0],
                      None,
                      None,
                      None]})
        meta_df = meta_df.set_index('field')
        return meta_df

    def prune_data(self, prune_pressure_list):
        pruned_profile = pd.DataFrame()
        for prune_pressure in prune_pressure_list:
            idx = self.df['pressure'].sub(prune_pressure).abs().argmin()
            pruned_profile = pruned_profile.append(self.df.iloc[idx], ignore_index=True)
        pruned_profile.drop_duplicates(subset=['pressure'])
        return pruned_profile


if __name__ == '__main__':
    sonde = WyomingUpperAirSonde(date=datetime(2021, 9, 20, 0), station='03238')
    sonde.get_metadata()
