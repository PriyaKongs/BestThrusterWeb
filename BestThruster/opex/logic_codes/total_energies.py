import numpy as np
import pandas as pd


class VesselEnergySpent:

    def __init__(self, min_energy_data):
        self.min_energy_data = min_energy_data
        self._convert_to_numpy()

    def _convert_to_numpy(self):
        # Ensure the data are numpy arrays for proper indexing
        self.min_energy_data["vessel_Va"] = np.array(self.min_energy_data["vessel_Va"])
        self.min_energy_data["vessel_thrust_N"] = np.array(
            self.min_energy_data["vessel_thrust_N"]
        )
        self.min_energy_data["vessel_hours"] = np.array(
            self.min_energy_data["vessel_hours"]
        )
        self.min_energy_data["P1"] = np.array(self.min_energy_data["P1"])
        self.min_energy_data["P2"] = np.array(self.min_energy_data["P2"])
        self.min_energy_data["P3"] = np.array(self.min_energy_data["P3"])

        self.min_energy_data["RPM"] = np.array(self.min_energy_data["RPM"])
        self.min_energy_data["torque"] = np.array(self.min_energy_data["torque"])

    def cal_energy_vessel_profile(self):
        # Masks for transit and bollard conditions
        transit_mask = self.min_energy_data["vessel_Va"] > 0
        bollard_mask = ~transit_mask & (self.min_energy_data["vessel_thrust_N"] > 0)

        # Extracting relevant columns
        self.vessel_hours = self.min_energy_data["vessel_hours"]
        self.vessel_P1 = self.min_energy_data["P1"]
        self.vessel_P2 = self.min_energy_data["P2"]
        self.vessel_P3 = self.min_energy_data["P3"]

        # Calculating transit and bollard energy
        self.min_energy_data["transit_energy_without_auxiliary"] = (
            self.vessel_P3[transit_mask] * self.vessel_hours[transit_mask]
        ).sum() / 1000
        self.min_energy_data["transit_energy_with_auxiliary"] = (
            self.min_energy_data["transit_energy_without_auxiliary"]
            + (
                self.min_energy_data["thruster_auxiliary"]
                * self.vessel_hours[transit_mask]
            ).sum()
            / 1000
        )
        self.min_energy_data["bollard_energy_without_auxiliary"] = (
            self.vessel_P3[bollard_mask] * self.vessel_hours[bollard_mask]
        ).sum() / 1000
        self.min_energy_data["bollard_energy_with_auxiliary"] = (
            self.min_energy_data["bollard_energy_without_auxiliary"]
            + (
                self.min_energy_data["thruster_auxiliary"]
                * self.vessel_hours[bollard_mask]
            ).sum()
            / 1000
        )

        # Total energy calculations
        self.min_energy_data["total_energy_without_auxiliary"] = (
            self.min_energy_data["transit_energy_without_auxiliary"]
            + self.min_energy_data["bollard_energy_without_auxiliary"]
        )
        self.min_energy_data["total_energy_with_auxiliary"] = (
            self.min_energy_data["transit_energy_with_auxiliary"]
            + self.min_energy_data["bollard_energy_with_auxiliary"]
        )

        # Propeller energy calculations
        self.min_energy_data["transit_propeller_energy"] = (
            self.vessel_P1[transit_mask] * self.vessel_hours[transit_mask]
        ).sum() / 1000
        self.min_energy_data["bollard_propeller_energy"] = (
            self.vessel_P1[bollard_mask] * self.vessel_hours[bollard_mask]
        ).sum() / 1000
        self.min_energy_data["total_propeller_energy"] = (
            self.min_energy_data["transit_propeller_energy"]
            + self.min_energy_data["bollard_propeller_energy"]
        )

        # Mechanical loss calculations
        self.min_energy_data["transit_mechanical_loss"] = (
            (self.vessel_P2[transit_mask] - self.vessel_P1[transit_mask])
            * self.vessel_hours[transit_mask]
        ).sum() / 1000
        self.min_energy_data["bollard_mechanical_loss"] = (
            (self.vessel_P2[bollard_mask] - self.vessel_P1[bollard_mask])
            * self.vessel_hours[bollard_mask]
        ).sum() / 1000
        self.min_energy_data["total_mechanical_loss"] = (
            self.min_energy_data["transit_mechanical_loss"]
            + self.min_energy_data["bollard_mechanical_loss"]
        )

        # Electrical loss calculations
        self.min_energy_data["transit_electrical_loss"] = (
            (self.vessel_P3[transit_mask] - self.vessel_P2[transit_mask])
            * self.vessel_hours[transit_mask]
        ).sum() / 1000
        self.min_energy_data["bollard_electrical_loss"] = (
            (self.vessel_P3[bollard_mask] - self.vessel_P2[bollard_mask])
            * self.vessel_hours[bollard_mask]
        ).sum() / 1000
        self.min_energy_data["total_electrical_loss"] = (
            self.min_energy_data["transit_electrical_loss"]
            + self.min_energy_data["bollard_electrical_loss"]
        )

        # Auxiliary loss calculations
        self.min_energy_data["transit_auxiliary_loss"] = (
            self.min_energy_data["thruster_auxiliary"] * self.vessel_hours[transit_mask]
        ).sum() / 1000
        self.min_energy_data["bollard_auxiliary_loss"] = (
            self.min_energy_data["thruster_auxiliary"] * self.vessel_hours[bollard_mask]
        ).sum() / 1000
        self.min_energy_data["total_auxiliary_loss"] = (
            self.min_energy_data["transit_auxiliary_loss"]
            + self.min_energy_data["bollard_auxiliary_loss"]
        )

        # Non-compliance calculations
        total_hours = self.vessel_hours.sum()
        over_power_mask = self.vessel_P3 > self.min_energy_data["thruster_max_power"]
        over_rpm_mask = (
            self.min_energy_data["RPM"] > self.min_energy_data["thruster_max_rpm"]
        )
        over_torque_mask = (
            self.min_energy_data["torque"] > self.min_energy_data["thruster_max_torque"]
        )

        self.min_energy_data["non_comp_power_percentage"] = (
            self.vessel_hours[over_power_mask].sum() / total_hours
        ) * 100
        self.min_energy_data["non_comp_rpm_percentage"] = (
            self.vessel_hours[over_rpm_mask].sum() / total_hours
        ) * 100
        self.min_energy_data["non_comp_torque_percentage"] = (
            self.vessel_hours[over_torque_mask].sum() / total_hours
        ) * 100

        overall_compliance_mask = over_power_mask | over_rpm_mask | over_torque_mask
        self.min_energy_data["non_compliance_hours"] = self.vessel_hours[
            overall_compliance_mask
        ].sum()
        self.min_energy_data["non_compliance_percentage"] = (
            self.min_energy_data["non_compliance_hours"] / total_hours
        ) * 100

        return self.min_energy_data
