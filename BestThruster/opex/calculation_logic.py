def calculate_best_thruster(
    vessel_name,
    auxiliary_consumption,
    port_mode_prop,
    bollard_mode_prop,
    transit_mode_prop,
    selected_thrusters,
):
    results = [
        {
            "rank": 1,
            "thruster": selected_thrusters,
            "bollard": bollard_mode_prop,
            "transit": transit_mode_prop,
            "total": 30,
            "auxiliary": 5,
            "non_compliance": 2,
        },
        {
            "rank": 2,
            "thruster": selected_thrusters,
            "bollard": bollard_mode_prop,
            "transit": transit_mode_prop,
            "total": 34,
            "auxiliary": 6,
            "non_compliance": 3,
        },
    ]
    return results
