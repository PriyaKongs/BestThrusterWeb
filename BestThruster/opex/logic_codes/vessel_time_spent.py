# Import Django models
from ..models import Vessel
import ast
import numpy as np


class VesselTimeSpent:
    def __init__(self, vessel_name, threshold=0):
        self.vessel_name = vessel_name
        self.threshold = threshold
        self.total_time = 8760.0

        self.vessel_transit_time = 0
        self.vessel_bollard_time = 0
        self.vessel_port_time = 0

        self.transit_mode_prop = 0
        self.bollard_mode_prop = 0
        self.port_mode_prop = 0

    def vessel_profile(self):
        try:
            vessel = Vessel.objects.get(name=self.vessel_name)
        except Vessel.DoesNotExist:
            raise ValueError("Vessel not found")

        self.vessel_stw = np.array(ast.literal_eval(vessel.stw_knots))
        self.vessel_thrust = np.array(ast.literal_eval(vessel.thrust_kN))
        self.vessel_hours = np.array(ast.literal_eval(vessel.hours))
        return self.vessel_stw, self.vessel_thrust, self.vessel_hours

    def time_spent(self):
        self.vessel_profile()

        # Calculate transit time
        transit_mode_mask = self.vessel_stw > self.threshold
        self.vessel_transit_time = self.vessel_hours[transit_mode_mask].sum()

        # Calculate bollard time
        bollard_mode_mask = ~transit_mode_mask & (self.vessel_thrust > 0)
        self.vessel_bollard_time = self.vessel_hours[bollard_mode_mask].sum()

        # Calculate port time
        self.vessel_port_time = round(
            self.total_time - (self.vessel_transit_time + self.vessel_bollard_time), 1
        )
        return self.vessel_transit_time, self.vessel_bollard_time, self.vessel_port_time

    def time_proportion(self):
        self.time_spent()
        self.transit_mode_prop = round(self.vessel_transit_time * 100 / self.total_time)
        self.bollard_mode_prop = round(self.vessel_bollard_time * 100 / self.total_time)
        self.port_mode_prop = round(
            100 - (self.transit_mode_prop + self.bollard_mode_prop)
        )
        return self.transit_mode_prop, self.bollard_mode_prop, self.port_mode_prop
