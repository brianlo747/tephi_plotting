import sys
import array
import numpy as np


class AutoSat(object):

    def __init__(self, infile):
        self._from_dat(infile)

    def _from_dat(self, infile):
        with open(infile, "rb") as f:
            data = f.read()
        f.close()

        # Check system endianness
        endianness = sys.byteorder

        header = data[0:570]

        tab_header_bytes = array.array("B")
        tab_header_ints = array.array("h")
        tab_header_longs = array.array("i")

        tab_header_bytes.frombytes(
            header[40:72] + header[300:318] + header[364:402] + header[428:448] + header[472:570])

        tab_header_ints.frombytes(
            header[8:10] + header[14:32] + header[72:300] + header[318:320] + header[402:428] + header[448:472])

        tab_header_longs.frombytes(
            header[0:4] + header[4:8] + header[10:14] + header[32:40] + header[320:364])

        if endianness == 'little':
            tab_header_bytes.byteswap()
            tab_header_ints.byteswap()
            tab_header_longs.byteswap()

        self.filesize = tab_header_longs[0]
        self.max_data_recs = tab_header_longs[1]
        self.max_rec_len = tab_header_ints[0]
        self.num_data_recs_used = tab_header_ints[1]
        self.max_data_rec_len_used = tab_header_longs[2]
        self.head_size = tab_header_ints[2]
        self.num_head_recs = tab_header_ints[3]
        self.datetime_mod = tab_header_ints[4:10]
        self.expiry_time = tab_header_longs[3:5]
        # self.spare = tab_header_bytes[0:32]
        self.prod_ident = tab_header_ints[10]
        self.sat_ident = tab_header_ints[11:21]
        self.channel = tab_header_ints[21:31]
        self.trans_id = tab_header_ints[31:41]
        self.obs_time = tab_header_ints[41:101]
        self.nom_dt = tab_header_ints[101:111]
        self.ysize = tab_header_ints[111]
        self.xsize = tab_header_ints[112]
        self.miss_data_flag = tab_header_ints[112:123]
        self.img_desc = tab_header_bytes[32:50].tobytes()
        self.prod_nom_dt = tab_header_ints[124]
        self.projection = tab_header_longs[5]
        self.hemisphere = tab_header_longs[6]
        self.down_long = tab_header_longs[7]
        self.tl_lat = tab_header_longs[8]
        self.tl_long = tab_header_longs[9]
        self.bl_lat = tab_header_longs[10]
        self.bl_long = tab_header_longs[11]
        self.br_lat = tab_header_longs[12]
        self.br_long = tab_header_longs[13]
        self.tr_lat = tab_header_longs[14]
        self.tr_long = tab_header_longs[15]
        # self.spare = tab_header_bytes[50:86]
        self.img_type = tab_header_bytes[86:88].tobytes()
        self.pixratio = tab_header_ints[125]
        self.bits_per_pixel = tab_header_ints[126]
        self.raw_data_info = tab_header_ints[127]
        self.cal_info = tab_header_ints[128:138]
        self.map_background = tab_header_bytes[88:108].tobytes()
        self.compress_technique = tab_header_ints[138]
        self.compress_params = tab_header_ints[139:149]
        self.comp_ind = tab_header_ints[149]
        # self.spare = tab_header_bytes[108:206]

        if self.num_head_recs == 1:
            pad_bytes = self.max_rec_len - 570
        else:
            pad_bytes = 2 * self.max_rec_len - 570
        image = data[570 + pad_bytes:]

        sat_image_block = array.array("B")
        sat_image_block.frombytes(image)
        sat_image_block.byteswap()
        self.sat_image = np.array(sat_image_block[:]).reshape((self.ysize, self.xsize))

        self.obs_time_year = self.obs_time[0]
        self.obs_time_month = self.obs_time[1]
        self.obs_time_day = self.obs_time[2]
        self.obs_time_hour = self.obs_time[3]
        self.obs_time_minute = self.obs_time[4]
        self.obs_time_second = self.obs_time[5]


if __name__ == '__main__':
    AutoSat(infile='/Users/brianlo/Desktop/Reading/PhD/WCD/data/eieu502107090100.dat')
