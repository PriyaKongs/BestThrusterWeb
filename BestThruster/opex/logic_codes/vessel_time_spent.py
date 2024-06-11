# Import Django models
from ..models import Vessel
import ast
import numpy as np


class VesselTimeSpent:
    """
    Class to calculate the time spent by a vessel in different operational modes.
    """

    def __init__(self, vessel_name, threshold=0):
        """
        Initialize the VesselTimeSpent class.

        :param vessel_name: Name of the vessel.
        :param threshold: Speed threshold to distinguish between transit and other modes.
        """

        self.vessel_name = vessel_name
        self.threshold = threshold
        self.total_time = 8760.0

        self.vessel_transit_time = 0
        self.vessel_bollard_time = 0
        self.vessel_port_time = 0

        self.transit_mode_prop = 0
        self.bollard_mode_prop = 0
        self.port_mode_prop = 0

    def time_spent(self):
        try:
            vessel = Vessel.objects.get(name=self.vessel_name)
            vessel_stw = ast.literal_eval(vessel.stw_knots)
            vessel_thrust = ast.literal_eval(vessel.thrust_kN)
            vessel_hours = ast.literal_eval(vessel.hours)
        except Vessel.DoesNotExist:
            raise ValueError("Vessel not found")

        vessel_stw = np.array(vessel_stw)
        vessel_thrust = np.array(vessel_thrust)
        vessel_hours = np.array(vessel_hours)

        # Calculate transit time
        transit_mode_mask = vessel_stw > self.threshold
        self.vessel_transit_time = vessel_hours[transit_mode_mask].sum()

        # Calculate bollard time
        bollard_mode_mask = ~transit_mode_mask & (vessel_thrust > 0)
        self.vessel_bollard_time = vessel_hours[bollard_mode_mask].sum()

        # Calculate port time
        self.vessel_port_time = round(
            (self.total_time - (self.vessel_transit_time + self.vessel_bollard_time)), 1
        )
        return self.vessel_transit_time, self.vessel_bollard_time, self.vessel_port_time

    def time_proportion(self):
        self.time_spent()
        self.transit_mode_prop = round(
            (self.vessel_transit_time * 100 / self.total_time)
        )
        self.bollard_mode_prop = round(
            (self.vessel_bollard_time * 100 / self.total_time)
        )
        self.port_mode_prop = round(
            100 - (self.transit_mode_prop + self.bollard_mode_prop)
        )
        return (
            self.transit_mode_prop,
            self.bollard_mode_prop,
            self.port_mode_prop,
        )

    # def hour_data_user_modi(self):
    #     self.time_proportion()
    #     self.total_user_bollard_time = self.total_time * float(self.pct_bollard) / 100.0
    #     self.total_user_transit_time = self.total_time * float(self.pct_transit) / 100.0
    #     self.total_user_port_time = self.total_time - (
    #         self.total_user_bollard_time + self.total_user_transit_time
    #     )

    #     transit_mask = self.vessel_profile["Va"] != 0

    #     mode_proportion_transit = (
    #         self.vessel_profile.loc[transit_mask, "hours"]
    #         / self.total_original_transit_time
    #     )
    #     mode_proportion_bollard = (
    #         self.vessel_profile.loc[~transit_mask, "hours"]
    #         / self.total_original_bollard_time
    #     )

    #     self.vessel_profile.loc[transit_mask, "hours"] = (
    #         mode_proportion_transit * self.total_user_transit_time
    #     )
    #     self.vessel_profile.loc[~transit_mask, "hours"] = (
    #         mode_proportion_bollard * self.total_user_bollard_time
    #     )

    #     self.vessel_profile.loc[0, "hours"] = self.total_user_port_time
    #     self.vessel_profile.loc[0, "Total port time"] = self.total_user_port_time
    #     self.vessel_profile.loc[0, "Total transit time"] = self.total_user_transit_time
    #     self.vessel_profile.loc[0, "Total bollard time"] = self.total_user_bollard_time

    #     return self.vessel_profile
