import datetime

import iris
import cftime


def print_cube_menu(model_filepath):
    # print(iris.load(model_filepath))
    return iris.load(model_filepath)
    # if standard_name is not None:
    #     constraint = iris.NameConstraint(standard_name=standard_name)
    #     selected_cubes = iris.load(model_filepath, constraint)
    #     for sc in selected_cubes:
    #         print(sc)


if __name__ == '__main__':
    model_filepath = '/Users/brianlo/Downloads/hourly_other_inc_theta_cb108_2014_fb_28_29.pp'
    datetime_start = cftime.Datetime360Day(2014, 2, 28)
    datetime_end = cftime.Datetime360Day(2014, 2, 29)
    constraint = iris.Constraint(time=lambda cell: datetime_start < cell.point < datetime_end)
    selected_cubes = iris.load(model_filepath, constraint)
    print(selected_cubes)
