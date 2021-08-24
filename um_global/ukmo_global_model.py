import datetime

import iris

from errors.io import PressureLevelNotFound


class UkmoGlobalModel(object):
    """
    This class contains the UKMO Global Model output data
    """

    def __init__(self, model_filepath):
        """
        Initialises UkmoGlobalModel object to store relevant data
        :param model_filepath: Filepath to relevant .pp file
        :type model_filepath: str
        """
        self.model_filepath = model_filepath
        self.iris_cubes = {}

    def print_cube_menu(self, standard_name=None):
        print(iris.load(self.model_filepath))
        if standard_name is not None:
            constraint = iris.NameConstraint(standard_name=standard_name)
            selected_cubes = iris.load(self.model_filepath, constraint)
            for sc in selected_cubes:
                print(sc)

    def read_dataset(self, standard_name=None, stash_code=None, cell_method=None,
                     lonlat_bounds=(-120, 50, 20, 90),
                     pressure_level=None):

        # Standard_name or stash_code
        if stash_code is not None:
            constraint = iris.NameConstraint(STASH=stash_code)
        else:
            constraint = iris.NameConstraint(standard_name=standard_name)

        # Cell Method
        if cell_method is not None:
            datetime_obj = iris.load(self.model_filepath, constraint)[0].coord('time')
            latest_dt = datetime_obj.points[-1]
            datetime_string = datetime_obj.units.num2date(latest_dt).strftime('%Y-%m-%d (%a) %H:%M:%SZ')
            latest_dt = datetime.datetime.strptime(datetime_string, '%Y-%m-%d (%a) %H:%M:%SZ')
            datetime_positive = latest_dt + datetime.timedelta(minutes=1)
            datetime_negative = latest_dt - datetime.timedelta(minutes=1)
            constraint = constraint & iris.Constraint(
                time=lambda cell: datetime_negative <= cell.point < datetime_positive)
            selected_cubes = iris.load(self.model_filepath, constraint)
            for idx, sc in enumerate(selected_cubes):
                if any(cm.method == cell_method for cm in sc.cell_methods):
                    iris_loaded_cube = sc
                    break
                elif sc.cell_methods == () and cell_method == '':
                    iris_loaded_cube = sc
                    break

        else:
            try:
                iris_loaded_cube = iris.load_cubes(self.model_filepath, constraint)
            except iris.exceptions.ConstraintMismatchError as cme:
                print(f"You have selected more than one cube! "
                      f"Here are the available cubes you could further constrain using cell_method...\n")
                for ic in iris.load(self.model_filepath, constraint):
                    print(ic)
                raise cme

        # LonLat selection
        if lonlat_bounds is not None:
            iris_loaded_cube = iris_loaded_cube.intersection(
                longitude=(lonlat_bounds[0], lonlat_bounds[1]), latitude=(lonlat_bounds[2], lonlat_bounds[3]))

        # Pressure level
        if pressure_level is not None:
            try:
                pressure_coords = iris_loaded_cube.coord('pressure')
            except iris.exceptions.CoordinateNotFoundError as iris_cnfe:
                print("There is no pressure coordinate in this cube! You cannot use select_pressure_level().")
                raise iris_cnfe

            constraint = iris.Constraint(pressure=pressure_level)
            try:
                if iris_loaded_cube.extract(constraint) is None:
                    raise PressureLevelNotFound(f"Pressure level {pressure_level}hPa does not exist!")
                else:
                    self.iris_cubes[f"{standard_name}_{pressure_level}hPa"] = iris_loaded_cube.extract(constraint)
            except PressureLevelNotFound as plnf:
                print(f"Pressure level {pressure_level}hPa does not exist!")
                print(f"Here are the available pressure levels:")
                print(f"{pressure_coords}")
                raise plnf

        else:
            if cell_method is None or cell_method == '':
                self.iris_cubes[f"{standard_name}"] = iris_loaded_cube
            else:
                self.iris_cubes[f"{standard_name}_{cell_method}"] = iris_loaded_cube

    def convert_units(self, field_name, new_units):
        self.iris_cubes[field_name].convert_units(new_units)

    def calculate_thickness(self, top_p_level=500, bottom_p_level=1000):
        thickness_field = self.iris_cubes[f"geopotential_height_{top_p_level}hPa"] - \
                          self.iris_cubes[f"geopotential_height_{bottom_p_level}hPa"]

        thickness_field.long_name = f"thickness_{bottom_p_level}_{top_p_level}hPa"
        self.iris_cubes[f"thickness_{bottom_p_level}_{top_p_level}hPa"] = thickness_field

    def calculate_total_rainfall_rate(self):
        tot_pptn_field = self.iris_cubes[f"convective_rainfall_flux"] + \
                         self.iris_cubes[f"stratiform_rainfall_flux"]
        self.iris_cubes[f"total_rainfall_rate"] = tot_pptn_field


if __name__ == '__main__':
    global_model_obj = UkmoGlobalModel('/Users/brianlo/Desktop/Reading/PhD/WCD/data/prods_op_gl-mn_20210708_00_000.pp')
    global_model_obj.print_cube_menu(standard_name='stratiform_rainfall_flux')
    # global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=1000)
    # global_model_obj.read_dataset('geopotential_height', cell_method='', pressure_level=500)
    # global_model_obj.calculate_thickness(500, 1000)

    # global_model_obj.read_dataset('geopotential_height', cell_method='mean')
    # print(global_model_obj.iris_cubes)
