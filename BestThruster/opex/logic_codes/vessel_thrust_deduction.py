class VesselProfileThrustDeduction:
    def __init__(
        self,
        thruster_profile,
        vessel_profile,
        threshold=0,
    ):
        self.thruster_profile = thruster_profile
        self.vessel_profile = vessel_profile
        self.threshold = threshold

    def thrust_deduction(self):
        self.vessel_stw = self.vessel_profile["vessel_stw"]
        self.vessel_thrust_N = self.vessel_profile["vessel_thrust_N"]
        self.vessel_Va = self.vessel_profile["vessel_Va"]
        self.thruster_thrust_deduction = self.thruster_profile["thrust_deduction"]
        self.thruster_wake_factor = self.thruster_profile["wake_factor"]

        transit_mode_mask = self.vessel_stw > self.threshold
        self.vessel_thrust_N[transit_mode_mask] = self.vessel_thrust_N[
            transit_mode_mask
        ] / (1 - self.thruster_thrust_deduction)
        self.vessel_Va[transit_mode_mask] *= 1 - self.thruster_wake_factor
        self.vessel_profile["thruster_auxiliary"] = self.thruster_profile[
            "auxiliary_consumption_kW"
        ]
        self.vessel_profile["thruster_max_power"] = self.thruster_profile["max_power"]
        self.vessel_profile["thruster_max_rpm"] = self.thruster_profile["max_rpm"]
        self.vessel_profile["thruster_max_torque"] = self.thruster_profile["max_torque"]

        return self.vessel_profile
