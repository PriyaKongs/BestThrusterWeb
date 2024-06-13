from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import ThrusterForm
from .calculation_logic import CalculationResults

from .logic_codes.vessel_time_spent import VesselTimeSpent

from .logic_codes.vessel_data_modified import VesselDataModification


def process_thruster_form_data(request, form):
    auxiliary_consumption_read = form.cleaned_data["auxiliary_consumption"]
    port_mode_prop_read = form.cleaned_data["port_mode_prop"]
    bollard_mode_prop_read = form.cleaned_data["bollard_mode_prop"]
    transit_mode_prop_read = form.cleaned_data["transit_mode_prop"]
    selected_thrusters_read = form.cleaned_data["thruster_options"]

    vessel_data = request.session.get("vessle_data")

    vessel_modified = VesselDataModification(
        vessel_data, port_mode_prop_read, bollard_mode_prop_read, transit_mode_prop_read
    )
    vessel_profile = vessel_modified.vess_data_unit_change()

    results_class = CalculationResults(
        selected_thrusters_read, vessel_profile, auxiliary_consumption_read
    )
    results = results_class.calculate_best_thruster()

    return results


def index(request):
    if request.method == "POST":
        form = ThrusterForm(request.POST)
        if form.is_valid():
            results = process_thruster_form_data(request, form)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "html": render_to_string(
                            "opex/results_partial.html", {"results": results}, request
                        )
                    }
                )
            return render(request, "opex/results.html", {"results": results})
    else:
        form = ThrusterForm()

    return render(request, "opex/index.html", {"form": form})


def get_vessel_modes(request):
    vessel_name = request.GET.get("vessel_name")
    if vessel_name:
        time_proportions = VesselTimeSpent(vessel_name)
        transit_mode_prop, bollard_mode_prop, port_mode_prop = (
            time_proportions.time_proportion()
        )
        vessel_transit_time, vessel_bollard_time, vessel_port_time = (
            time_proportions.time_spent()
        )
        vessle_stw, vessle_thrust, vessle_hours = time_proportions.vessel_profile()

        # Convert NumPy arrays to lists
        vessle_data = {
            "vessel_stw": vessle_stw.tolist(),
            "vessel_thrust": vessle_thrust.tolist(),
            "vessel_hours": vessle_hours.tolist(),
            "transit_mode_original": transit_mode_prop,
            "bollard_mode_original": bollard_mode_prop,
            "port_mode_original": port_mode_prop,
            "transit_time_original": vessel_transit_time,
            "bollard_time_original": vessel_bollard_time,
            "port_time_original": vessel_port_time,
        }

        # Store vessle_data in session
        request.session["vessle_data"] = vessle_data

        data = {
            "transit_mode_prop": transit_mode_prop,
            "bollard_mode_prop": bollard_mode_prop,
            "port_mode_prop": port_mode_prop,
        }
    else:
        data = {
            "transit_mode_prop": "",
            "bollard_mode_prop": "",
            "port_mode_prop": "",
        }
    return JsonResponse(data)
