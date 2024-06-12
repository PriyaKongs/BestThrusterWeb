import numpy as np
import copy


class VesselDataModification:

    def __init__(
        self,
        vessel_data,
        port_mode_prop_read,
        bollard_mode_prop_read,
        transit_mode_prop_read,
        threshold=0,
    ):
        self.vessel_data = vessel_data
        self.port_mode_prop_read = port_mode_prop_read
        self.bollard_mode_prop_read = bollard_mode_prop_read
        self.transit_mode_prop_read = transit_mode_prop_read
        self.threshold = threshold
        self.total_time = 8760.0

    def hour_data_user_modi(self):
        self.vessel_stw = np.array(self.vessel_data["vessel_stw"])
        self.vessel_thrust = np.array(self.vessel_data["vessel_thrust"])
        self.vessel_hours = np.array(self.vessel_data["vessel_hours"])

        self.total_user_bollard_time = (
            self.total_time * float(self.bollard_mode_prop_read) / 100.0
        )
        self.total_user_transit_time = (
            self.total_time * float(self.transit_mode_prop_read) / 100.0
        )
        self.total_user_port_time = self.total_time - (
            self.total_user_bollard_time + self.total_user_transit_time
        )
        transit_mode_mask = self.vessel_stw > self.threshold
        bollard_mode_mask = ~transit_mode_mask & (self.vessel_thrust > 0)

        mode_proportion_transit = (
            self.vessel_hours[transit_mode_mask]
            / self.vessel_data["transit_time_original"]
        )
        mode_proportion_bollard = (
            self.vessel_hours[bollard_mode_mask]
            / self.vessel_data["bollard_time_original"]
        )

        self.vessel_hours[transit_mode_mask] = (
            mode_proportion_transit * self.total_user_transit_time
        )

        self.vessel_hours[bollard_mode_mask] = (
            mode_proportion_bollard * self.total_user_bollard_time
        )

        self.vessel_hours[0] = self.total_user_port_time
        self.vessel_hours = np.array(self.vessel_hours)

    def vess_data_unit_change(self):
        self.hour_data_user_modi()

        self.vessel_thrust_N = self.vessel_thrust * 1000.0
        self.vessel_stw_MpS = self.vessel_stw * 1852.0 / 3600.0
        self.vessel_Va = copy.deepcopy(self.vessel_stw_MpS)

        vessel_profile = {
            "vessel_stw": np.array(self.vessel_stw),
            "vessel_thrust": np.array(self.vessel_thrust),
            "vessel_hours": np.array(self.vessel_hours),
            "vessel_thrust_N": np.array(self.vessel_thrust_N),
            "vessel_stw_MpS": np.array(self.vessel_stw_MpS),
            "vessel_Va": np.array(self.vessel_Va),
            "transit_time": self.total_user_transit_time,
            "bollard_time": self.total_user_bollard_time,
            "port_time": self.total_user_port_time,
        }

        return vessel_profile
