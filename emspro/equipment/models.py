
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date

class Workshop(models.Model):
    name = models.CharField(max_length=255,unique=True)
    location = models.CharField(max_length=255,default='local')
    status = models.CharField(max_length=255,default='active')
    description = models.CharField(max_length=100,null=True)  # Corrected spelling
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)


class EnergySource(models.Model):
    type = models.CharField(max_length=100, default='default_type')
    supplier = models.CharField(max_length=100, default='default_supplier')
    current_reservation = models.FloatField(default=0.0)
    price = models.FloatField(blank=True, null=True)
    level = models.IntegerField(default=3)
    energy_code = models.CharField(max_length=100,default='default_code')
    coal_discount_factor = models.FloatField(default=1)
    carbon_emission_factor = models.FloatField( default=1)
    unit = models.CharField(max_length=100,default='Kwh')
    description = models.CharField(max_length=100,null=True)
    create_user = models.CharField(max_length=100,default='admin')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

class Equipment(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=100, default='default_type')  # Default value for 'type'
    status = models.BooleanField(default=True)
    energy_type = models.CharField(max_length=100, default='default_energy')  # Default value for 'energy_type'
    volume = models.FloatField(blank=True, null=True)
    electric = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    actual_rate = models.FloatField(blank=True, null=True)
    standard_rate = models.FloatField(blank=True,default=0.0000205)
    url = models.CharField(max_length=2000,null=True)
    gbl_file_name = models.CharField(max_length=2000,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

class EnergyConsumption(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='consumptions')
    energy_loss = models.FloatField(blank=True, null=True)
    in_energy_source = models.ForeignKey('EnergySource', on_delete=models.CASCADE, related_name='in_consumptions')
    in_energy_quantity = models.FloatField()
    energy_used = models.FloatField(blank=True, null=True)
    expect_use = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    expect_cost = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

class AlarmRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='alarm_records')
    energy_consumption = models.ForeignKey(EnergyConsumption, on_delete=models.CASCADE, default=1,related_name='alarm')
    maintenance_type = models.ForeignKey('MaintenanceRecord', on_delete=models.CASCADE, default=1,related_name='alarm')
    details = models.TextField(default='No details provided.')  # Default value for 'details'
    alarm_type = models.CharField(max_length=100, default='default_type')
    alarm_status = models.CharField(max_length=100, default='default_status')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)


class MaintenanceRecord(models.Model):
    energy_consumption = models.ForeignKey(EnergyConsumption, on_delete=models.CASCADE,default=1)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records')
    operator = models.CharField(max_length=100, default='Unknown Operator')  # Default value for 'operator'
    details = models.TextField(default='No details provided.')  # Default value for 'details'
    status = models.CharField(max_length=100, default='Pending')  # Default value for 'status'
    scheduled_date = models.DateTimeField(auto_now=True)
    maintenance_type = models.CharField(max_length=100,default='regular_maintenance')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

class EnergyPlan(models.Model):
    PLAN_INTERVALS = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    energy_type = models.ForeignKey('EnergySource', on_delete=models.CASCADE)
    intervals = models.CharField(max_length=10, choices=PLAN_INTERVALS)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    energy_target = models.FloatField()  # Target energy consumption for the period
    description = models.TextField(blank=True)  # Optional field for describing the plan or target

