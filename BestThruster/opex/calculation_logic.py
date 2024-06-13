import pandas as pd
import copy
from .logic_codes.thruster_data_modified import ThrusterProfileCalcs
from .logic_codes.vessel_thrust_deduction import VesselProfileThrustDeduction
from .logic_codes.minimum_power_calc import MinimumPower
from .logic_codes.total_energies import VesselEnergySpent


class CalculationResults:
    def __init__(
        self, selected_thrusters_read, vessel_profile, auxiliary_consumption_read
    ):
        self.selected_thrusters_read = selected_thrusters_read
        self.vessel_profile = vessel_profile
        self.auxiliary_consumption_read = auxiliary_consumption_read

    def calculate_best_thruster(self):
        thruster_energy_data_dictionary = {
            "thruster": [],
            "bollard": [],
            "transit": [],
            "total": [],
            "auxi": [],
            "compliancy": [],
        }

        for thruster_name in self.selected_thrusters_read:
            temp = copy.deepcopy(self.vessel_profile)

            thruster_profile_class = ThrusterProfileCalcs(thruster_name)

            thruster_profile = thruster_profile_class.thruster_profile()

            thrust_deduced_class = VesselProfileThrustDeduction(
                thruster_profile=thruster_profile, vessel_profile=temp
            )
            vessel_profile_thrust_deduced = thrust_deduced_class.thrust_deduction()
            mini_pwr_class = MinimumPower(
                thruster_profile, vessel_profile_thrust_deduced
            )

            min_power_vessel_profile = mini_pwr_class.update_data()

            vessel_energy_class = VesselEnergySpent(min_power_vessel_profile)

            vessel_energy = vessel_energy_class.cal_energy_vessel_profile()

            thruster_energy_data_dictionary["thruster"].append(thruster_name)

            if self.auxiliary_consumption_read == "Yes":
                thruster_energy_data_dictionary["bollard"].append(
                    round(vessel_energy["bollard_energy_with_auxiliary"])
                )
                thruster_energy_data_dictionary["transit"].append(
                    round(vessel_energy["transit_energy_with_auxiliary"])
                )
                thruster_energy_data_dictionary["total"].append(
                    round(vessel_energy["total_energy_with_auxiliary"])
                )

                thruster_energy_data_dictionary["auxi"].append(
                    round(vessel_energy["total_auxiliary_loss"])
                )
            else:
                thruster_energy_data_dictionary["bollard"].append(
                    round(vessel_energy["bollard_energy_without_auxiliary"])
                )
                thruster_energy_data_dictionary["transit"].append(
                    round(vessel_energy["transit_energy_without_auxiliary"])
                )
                thruster_energy_data_dictionary["total"].append(
                    round(vessel_energy["total_energy_without_auxiliary"])
                )

                thruster_energy_data_dictionary["auxi"].append(0)

            thruster_energy_data_dictionary["compliancy"].append(
                round(vessel_energy["non_compliance_percentage"], 2)
            )
        thruster_energy_data_dataframe = pd.DataFrame(thruster_energy_data_dictionary)
        sorted_thruster_energy_data_dataframe = (
            thruster_energy_data_dataframe.sort_values(by="total", ascending=True)
        )

        results = []
        for rank, row in enumerate(
            sorted_thruster_energy_data_dataframe.itertuples(), start=1
        ):
            results.append(
                {
                    "rank": rank,
                    "thruster": row.thruster,
                    "bollard": row.bollard,
                    "transit": row.transit,
                    "total": row.total,
                    "auxiliary": row.auxi,
                    "non_compliance": row.compliancy,
                }
            )
        return results
