from django.http import JsonResponse
from django.shortcuts import render
from .forms import ThrusterForm
from .calculation_logic import calculate_best_thruster
from .models import Vessel, Thruster
from .logic_codes.vessel_time_spent import VesselTimeSpent


def index(request):
    if request.method == "POST":
        form = ThrusterForm(request.POST)
        if form.is_valid():
            vessel_name = form.cleaned_data["vessel_name"]
            auxiliary_consumption = form.cleaned_data["auxiliary_consumption"]
            port_mode_prop = form.cleaned_data["port_mode_prop"]
            bollard_mode_prop = form.cleaned_data["bollard_mode_prop"]
            transit_mode_prop = form.cleaned_data["transit_mode_prop"]
            selected_thrusters = form.cleaned_data["thruster_options"]
            print("we can get user modifed time")
            print(port_mode_prop, bollard_mode_prop, transit_mode_prop)

            ts = VesselTimeSpent(vessel_name)
            transit_mode_prop, bollard_mode_prop, port_mode_prop = ts.time_proportion()

            results = calculate_best_thruster(
                vessel_name,
                auxiliary_consumption,
                port_mode_prop,
                bollard_mode_prop,
                transit_mode_prop,
                selected_thrusters,
            )

            return render(request, "opex/results.html", {"results": results})
    else:
        form = ThrusterForm()

    return render(request, "opex/index.html", {"form": form})


def get_vessel_modes(request):
    vessel_name = request.GET.get("vessel_name")
    if vessel_name:
        ts = VesselTimeSpent(vessel_name)
        transit_mode_prop, bollard_mode_prop, port_mode_prop = ts.time_proportion()
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
