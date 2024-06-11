# import os
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Thruster
# from .forms import CSVUploadForm
# from django.db import IntegrityError


# def parse_float(value):
#     try:
#         return float(value)
#     except (ValueError, TypeError):
#         return None


# def handle_csv_upload(request):
#     if request.method == "POST":
#         form = CSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = form.cleaned_data["csv_file"]
#             file_name = os.path.splitext(csv_file.name)[0]

#             # Read CSV using pandas
#             df = pd.read_csv(csv_file)
#             df.fillna(value=pd.NA, inplace=True)

#             for index, row in df.iterrows():
#                 try:
#                     Thruster.objects.create(
#                         name=file_name,
#                         motor_efficiency=[
#                             parse_float(x)
#                             for x in row.get("motor_efficiency", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         motor_load=[
#                             parse_float(x)
#                             for x in row.get("motor_load", "[]").strip("[]").split(",")
#                         ],
#                         P_D=[
#                             parse_float(x)
#                             for x in row.get("P_D", "[]").strip("[]").split(",")
#                         ],
#                         transist_j=[
#                             parse_float(x)
#                             for x in row.get("transist_j", "[]").strip("[]").split(",")
#                         ],
#                         transist_kt_tot=[
#                             parse_float(x)
#                             for x in row.get("transist_kt_tot", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         transist_kq10=[
#                             parse_float(x)
#                             for x in row.get("transist_kq10", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         propeller_rpm_1min=[
#                             parse_float(x)
#                             for x in row.get("propeller_rpm_1min", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         propeller_power_kw=[
#                             parse_float(x)
#                             for x in row.get("propeller_power_kw", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         thruster_efficiency_40c=[
#                             parse_float(x)
#                             for x in row.get("thruster_efficiency_40c", "[]")
#                             .strip("[]")
#                             .split(",")
#                         ],
#                         max_rpm=parse_float(row.get("max_rpm")),
#                         max_power=parse_float(row.get("max_power")),
#                         propeller_diameter=parse_float(row.get("propeller_diameter")),
#                         wake_factor=parse_float(row.get("wake_factor")),
#                         thrust_deduction=parse_float(row.get("thrust_deduction")),
#                         relative_rotative_efficiency=parse_float(
#                             row.get("relative_rotative_efficiency")
#                         ),
#                         auxiliary_consumption_kW=parse_float(
#                             row.get("auxiliary_consumption_kW")
#                         ),
#                     )
#                 except IntegrityError as e:
#                     messages.error(request, f"Error saving {file_name}: {e}")
#                     continue  # Skip the problematic row and continue with the next one

#             messages.success(request, "CSV file has been uploaded successfully.")
#             return redirect("admin:appname_thruster_changelist")
#     else:
#         form = CSVUploadForm()

#     context = {"form": form}
#     return render(request, "admin/csv_form.html", context)
