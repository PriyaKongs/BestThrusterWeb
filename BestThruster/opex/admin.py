from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
import json
from .models import Thruster, Vessel


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Thruster)
class ThrusterAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            file_name = csv_file.name.split(".")[0]
            df = pd.read_csv(csv_file)
            df.fillna(pd.NA, inplace=True)

            columns_with_lists = [
                "motor_efficiency",
                "motor_load",
                "P_D",
                "transist_j",
                "transist_kt_tot",
                "transist_kq10",
                "propeller_rpm_1min",
                "propeller_power_kW",
                "thruster_efficiency_40C",
            ]

            aggregated_data = {}
            for col in columns_with_lists:
                aggregated_data[col] = df[col].dropna().tolist()

            try:
                thruster = Thruster(
                    name=file_name,
                    motor_efficiency=json.dumps(aggregated_data["motor_efficiency"]),
                    motor_load=json.dumps(aggregated_data["motor_load"]),
                    P_D=json.dumps(aggregated_data["P_D"]),
                    transist_j=json.dumps(aggregated_data["transist_j"]),
                    transist_kt_tot=json.dumps(aggregated_data["transist_kt_tot"]),
                    transist_kq10=json.dumps(aggregated_data["transist_kq10"]),
                    propeller_rpm_1min=json.dumps(
                        aggregated_data["propeller_rpm_1min"]
                    ),
                    propeller_power_kW=json.dumps(
                        aggregated_data["propeller_power_kW"]
                    ),
                    thruster_efficiency_40C=json.dumps(
                        aggregated_data["thruster_efficiency_40C"]
                    ),
                    max_rpm=(float(df["max_rpm"].dropna().iloc[0])),
                    max_power=(float(df["max_power"].dropna().iloc[0])),
                    propeller_diameter=(
                        float(df["propeller_diameter"].dropna().iloc[0])
                    ),
                    wake_factor=(float(df["wake_factor"].dropna().iloc[0])),
                    thrust_deduction=(float(df["thrust_deduction"].dropna().iloc[0])),
                    relative_rotative_efficiency=(
                        float(df["relative_rotative_efficiency"].dropna().iloc[0])
                    ),
                    auxiliary_consumption_kW=(
                        float(df["auxiliary_consumption_kW"].dropna().iloc[0])
                    ),
                )
                thruster.save()
                self.message_user(request, "Your CSV file has been imported")
            except Exception as e:
                messages.error(request, f"Error processing the file: {e}")

            return redirect("..")

        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.upload_csv_vessel),
        ]
        return custom_urls + urls

    def upload_csv_vessel(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            file_name = csv_file.name.split(".")[0]
            df = pd.read_csv(csv_file)
            df.fillna(pd.NA, inplace=True)

            df = df[df["hours"] != 0.0]
            df = df.reset_index(drop=True)

            columns_with_lists = [
                "thrust_kN",
                "stw_knots",
                "hours",
            ]

            aggregated_data = {}
            for col in columns_with_lists:
                aggregated_data[col] = df[col].dropna().tolist()

            try:
                vessel = Vessel(
                    name=file_name,
                    thrust_kN=json.dumps(aggregated_data["thrust_kN"]),
                    stw_knots=json.dumps(aggregated_data["stw_knots"]),
                    hours=json.dumps(aggregated_data["hours"]),
                )
                vessel.save()
                self.message_user(request, "Your CSV file has been imported")
            except Exception as e:
                messages.error(request, f"Error processing the file: {e}")

            return redirect("..")

        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)
