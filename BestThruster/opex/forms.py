from django import forms
from .models import Vessel, Thruster


class ThrusterForm(forms.Form):
    vessel_name = forms.ChoiceField(choices=[], required=True)
    auxiliary_consumption = forms.ChoiceField(choices=[("Yes", "Yes"), ("No", "No")])
    port_mode_prop = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"id": "port_mode_prop"}),
        label="Proportion of time in port mode",
    )
    bollard_mode_prop = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"id": "bollard_mode_prop"}),
        label="Proportion of time in bollard mode",
    )
    transit_mode_prop = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"id": "transit_mode_prop"}),
        label="Proportion of time in transit mode",
    )
    thruster_options = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, label="Select thrusters: "
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vessel_name"].choices = [
            ("", "Select a vessel")
        ] + self.get_vessel_choices()
        self.fields["thruster_options"].choices = self.get_thruster_choices()

    def get_vessel_choices(self):
        vessels = Vessel.objects.all()
        choices = [(vessel.name, vessel.name) for vessel in vessels]
        return choices

    def get_thruster_choices(self):
        thrusters = Thruster.objects.all()
        choices = [(thruster.name, thruster.name) for thruster in thrusters]
        return choices
