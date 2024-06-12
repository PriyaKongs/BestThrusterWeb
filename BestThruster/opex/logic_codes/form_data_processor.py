from ..calculation_logic import calculate_best_thruster
from .vessel_data_modified import VesselDataModification


def process_thruster_form_data(request, form):
    vessel_name = form.cleaned_data["vessel_name"]
    auxiliary_consumption = form.cleaned_data["auxiliary_consumption"]
    port_mode_prop_read = form.cleaned_data["port_mode_prop"]
    bollard_mode_prop_read = form.cleaned_data["bollard_mode_prop"]
    transit_mode_prop_read = form.cleaned_data["transit_mode_prop"]
    selected_thrusters = form.cleaned_data["thruster_options"]

    vessel_data = request.session.get("vessel_data")
    vessel_modified = VesselDataModification(vessel_data)
    print(vessel_data)

    results = calculate_best_thruster(
        vessel_name,
        auxiliary_consumption,
        port_mode_prop_read,
        bollard_mode_prop_read,
        transit_mode_prop_read,
        selected_thrusters,
    )

    return results
