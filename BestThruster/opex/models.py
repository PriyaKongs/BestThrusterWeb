from django.db import models


class Thruster(models.Model):
    name = models.CharField(max_length=255)
    motor_efficiency = models.JSONField()
    motor_load = models.JSONField()
    P_D = models.JSONField()
    transist_j = models.JSONField()
    transist_kt_tot = models.JSONField()
    transist_kq10 = models.JSONField()
    propeller_rpm_1min = models.JSONField()
    propeller_power_kW = models.JSONField()
    thruster_efficiency_40C = models.JSONField()
    max_rpm = models.FloatField()
    max_power = models.FloatField()
    propeller_diameter = models.FloatField()
    wake_factor = models.FloatField()
    thrust_deduction = models.FloatField()
    relative_rotative_efficiency = models.FloatField()
    auxiliary_consumption_kW = models.FloatField()

    def __str__(self):
        return self.name


class Vessel(models.Model):
    name = models.CharField(max_length=255)
    thrust_kN = models.JSONField()
    stw_knots = models.JSONField()
    hours = models.JSONField()

    def __str__(self):
        return self.name
