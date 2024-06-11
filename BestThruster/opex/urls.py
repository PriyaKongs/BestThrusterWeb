from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_vessel_modes/", views.get_vessel_modes, name="get_vessel_modes"),
]
