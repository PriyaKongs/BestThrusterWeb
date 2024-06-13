from scipy.interpolate import interp1d, griddata
import numpy as np


class DataUtils:

    def __init__(self, rho=1025):
        self.rho = rho

    def unique_values(self, key, data):
        return list(set(data[key]))

    def create_number_list(self, start_number, end_number, step):
        number_list = [
            round(i, 6) for i in np.arange(start_number, end_number + step, step)
        ]
        if number_list[-1] != end_number:
            number_list[-1] = round(end_number, 6)
        return number_list

    def interpolate_data(self, x_values, y_values):
        return interp1d(x_values, y_values, fill_value="extrapolate")

    def thruster_efficiency(
        self, propeller_rpm, propeller_power, thruster_efficiency, n_temp_min, P1
    ):

        return griddata(
            (propeller_rpm, propeller_power),
            thruster_efficiency,
            (n_temp_min, P1),
            fill_value=-1,
            method="nearest",
        )
