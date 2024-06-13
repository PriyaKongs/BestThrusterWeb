import pandas as pd
import numpy as np
from .utility_functions import DataUtils


class MinimumPower:

    def __init__(self, thruster, vessel):

        self.thruster = thruster
        self.vessel = vessel

        self.utils = DataUtils()
        self.rho = self.utils.rho
        self.unique_p_d = self.utils.unique_values("P_D", self.thruster)

    def update_data(self):
        self.initialize_new_columns()

        non_zero_indices = [i for i in range(len(self.vessel["vessel_Va"])) if i != 0]
        results = map(self.calculate_minimum_power, non_zero_indices)

        for idx, (min_pwr, rpm, torque, P1, P2, P_D) in zip(non_zero_indices, results):
            self.update_vessel_data(idx, min_pwr, rpm, torque, P1, P2, P_D)

        return self.vessel

    def initialize_new_columns(self):

        for column in ["P_D", "RPM", "torque", "P1", "P2", "P3"]:
            self.vessel[column] = [0.0] * len(self.vessel["vessel_Va"])

    def calculate_minimum_power(self, i):

        if i == 0:
            return 0, 0, 0, 0, 0, 0

        power_comp, rpm_comp, torque_comp, P1_comp, P2_comp, PD_comp = (
            self.calculate_power_components(i)
        )

        power_comp_filtered = [val for val in power_comp if not pd.isna(val)]
        if power_comp_filtered:
            min_power = min(power_comp_filtered)
            min_pwr_index = power_comp.index(min_power)
            return (
                min_power,
                rpm_comp[min_pwr_index],
                torque_comp[min_pwr_index],
                P1_comp[min_pwr_index],
                P2_comp[min_pwr_index],
                PD_comp[min_pwr_index],
            )
        else:
            return (
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            )

    def calculate_power_components(self, i):

        power_comp, rpm_comp, torque_comp, P1_comp, P2_comp, P_D_comp = (
            [],
            [],
            [],
            [],
            [],
            [],
        )

        for p_d in self.unique_p_d:
            subset = {
                key: [
                    self.thruster[key][index]
                    for index in range(len(self.thruster[key]))
                    if self.thruster["P_D"][index] == p_d
                ]
                for key in ["kt_j_sq", "transist_j", "transist_kq10", "transist_kt_tot"]
            }

            Kt_temp, Kq_temp, n_temp = self.calculate_KtKqN(i, subset)
            Q = (
                Kq_temp
                * self.rho
                * n_temp**2
                * self.thruster["propeller_diameter"] ** 5
                / self.thruster["relative_rotative_efficiency"]
            )
            P1 = Q * n_temp * 2 * np.pi / 1000
            n_temp_min = n_temp * 60
            thruster_efficiency_temp = self.utils.thruster_efficiency(
                self.thruster["propeller_rpm_1min"],
                self.thruster["propeller_power_kW"],
                self.thruster["thruster_efficiency_40C"],
                n_temp_min,
                P1,
            )
            P2 = P1 / thruster_efficiency_temp
            P2_rel = P2 / self.thruster["max_power"]
            motor_efficiency_temp = self.utils.interpolate_data(
                self.thruster["motor_load"], self.thruster["motor_efficiency"]
            )(P2_rel)
            pwr_to_compare = P2 / motor_efficiency_temp
            power_comp.append(pwr_to_compare)
            rpm_comp.append(P1 * 60 / (2 * np.pi * Q / 1000))
            torque_comp.append(Q / 1000)
            P1_comp.append(P1)
            P2_comp.append(P2)
            P_D_comp.append(p_d)

        return power_comp, rpm_comp, torque_comp, P1_comp, P2_comp, P_D_comp

    def calculate_KtKqN(self, i, subset):

        if self.vessel["vessel_Va"][i] != 0:
            return self.calculate_KtKqN_transit(i, subset)
        else:
            return self.calculate_KtKqN_Bollard(i, subset)

    def calculate_KtKqN_transit(self, i, subset):
        J2_KT_temp = self.vessel["vessel_thrust_N"][i] / (
            self.vessel["vessel_Va"][i] ** 2
            * self.rho
            * self.thruster["propeller_diameter"] ** 2
        )
        Kt_temp = self.utils.interpolate_data(subset["kt_j_sq"], subset["transist_j"])(
            J2_KT_temp
        )
        Kq_temp = (
            self.utils.interpolate_data(subset["transist_j"], subset["transist_kq10"])(
                Kt_temp
            )
            / 10
        )
        n_temp = self.vessel["vessel_Va"][i] / (
            Kt_temp * self.thruster["propeller_diameter"]
        )

        return Kt_temp, Kq_temp, n_temp

    def calculate_KtKqN_Bollard(self, i, subset):

        Kt_temp = subset["transist_kt_tot"][0]
        Kq_temp = subset["transist_kq10"][0] / 10
        n_temp = np.sqrt(
            self.vessel["vessel_thrust_N"][i]
            / (Kt_temp * self.rho * self.thruster["propeller_diameter"] ** 4)
        )

        return Kt_temp, Kq_temp, n_temp

    def update_vessel_data(self, i, min_pwr, rpm, torque, P1, P2, P_D):

        self.vessel["P3"][i] = min_pwr
        self.vessel["RPM"][i] = rpm
        self.vessel["torque"][i] = torque
        self.vessel["P1"][i] = P1
        self.vessel["P2"][i] = P2
        self.vessel["P_D"][i] = P_D

        return self.vessel
