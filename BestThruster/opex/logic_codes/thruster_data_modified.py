# Import Django models
from ..models import Thruster
import ast
import numpy as np


class ThrusterProfileCalcs:
    def __init__(self, thruster_name):
        self.thruster_name = thruster_name

    def thruster_profile(self):
        try:
            thruster = Thruster.objects.get(name=self.thruster_name)
        except Thruster.DoesNotExist:
            raise ValueError("Thruster not found")

        self.motor_efficiency = np.array(ast.literal_eval(thruster.motor_efficiency))
        self.motor_load = np.array(ast.literal_eval(thruster.motor_load))
        self.P_D = np.array(ast.literal_eval(thruster.P_D))
        self.transist_j = np.array(ast.literal_eval(thruster.transist_j))
        self.transist_kt_tot = np.array(ast.literal_eval(thruster.transist_kt_tot))
        self.transist_kq10 = np.array(ast.literal_eval(thruster.transist_kq10))
        self.propeller_rpm_1min = np.array(
            ast.literal_eval(thruster.propeller_rpm_1min)
        )
        self.propeller_power_kW = np.array(
            ast.literal_eval(thruster.propeller_power_kW)
        )
        self.thruster_efficiency_40C = np.array(
            ast.literal_eval(thruster.thruster_efficiency_40C)
        )
        self.max_rpm = thruster.max_rpm
        self.max_power = thruster.max_power
        self.propeller_diameter = thruster.propeller_diameter
        self.wake_factor = thruster.wake_factor
        self.thrust_deduction = thruster.thrust_deduction
        self.relative_rotative_efficiency = thruster.relative_rotative_efficiency
        self.auxiliary_consumption_kW = thruster.auxiliary_consumption_kW

        self.transist_j = np.where(
            self.transist_j == 0, self.transist_j + (0.1**10), self.transist_j
        )

        self.kt_j_sq = np.array(self.transist_kt_tot / self.transist_j**2)

        self.max_torque = self.max_power / (2 * np.pi * (self.max_rpm / 60))

        thruster_profile = {
            "motor_efficiency": self.motor_efficiency,
            "motor_load": self.motor_load,
            "P_D": self.P_D,
            "transist_j": self.transist_j,
            "transist_kt_tot": self.transist_kt_tot,
            "transist_kq10": self.transist_kq10,
            "propeller_rpm_1min": self.propeller_rpm_1min,
            "propeller_power_kW": self.propeller_power_kW,
            "thruster_efficiency_40C": self.thruster_efficiency_40C,
            "max_rpm": self.max_rpm,
            "max_power": self.max_power,
            "propeller_diameter": self.propeller_diameter,
            "wake_factor": self.wake_factor,
            "thrust_deduction": self.thrust_deduction,
            "relative_rotative_efficiency": self.relative_rotative_efficiency,
            "auxiliary_consumption_kW": self.auxiliary_consumption_kW,
            "kt_j_sq": self.kt_j_sq,
            "max_torque": self.max_torque,
        }
        return thruster_profile
