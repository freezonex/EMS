
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date

class Workshop(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def total_energy_consumption(self):
        # This fetches the total energy consumption for all equipment in this workshop
        return EnergyConsumption.objects.filter(
            equipment__workshop=self
        ).aggregate(total_energy=Sum('energy_used'))['total_energy'] or 0

    def total_expected_energy_consumption(self):
        # This fetches the total energy consumption for all equipment in this workshop
        return EnergyConsumption.objects.filter(
            equipment__workshop=self
        ).aggregate(total_expect_energy=Sum('expect_used'))['total_expect_energy'] or 0

    # def Oneday_energy_consumption(self, date=None,energy_type=None):
    #     if date is None:
    #         date = timezone.now().date()  # defaults to today if no date is provided
    #     # This calculates daily energy consumption for all equipment in this workshop
    #     return EnergyConsumption.objects.filter(
    #         equipment__workshop=self,
    #         create_time__date=date,
    #     ).aggregate(daily_energy=Sum('energy_used'))['daily_energy'] or 0
    #
    # def daily_energy_consumption(self, start_date=None, end_date=None, energy_type=None):
    #     # Ensure that dates are parsed if they are provided as strings
    #     if start_date and isinstance(start_date, str):
    #         start_date = parse_date(start_date)
    #     if end_date and isinstance(end_date, str):
    #         end_date = parse_date(end_date)
    #     elif not end_date:  # Default to today if no end date provided
    #         end_date = timezone.now().date()
    #
    #     # Build the base query
    #     consumptions = EnergyConsumption.objects.filter(equipment__workshop=self)
    #
    #     # Apply date range filter only if a start date is provided
    #     if start_date==None:
    #         start_date = parse_date("2024-05-21")
    #         consumptions = consumptions.filter(create_time__date__range=(start_date, end_date))
    #     else:
    #         consumptions = consumptions.filter(create_time__date__range=(start_date, end_date))
    #
    #     # Filter by energy type if provided
    #     if energy_type!=None:
    #         consumptions = consumptions.filter(energy_type=energy_type)
    #
    #     # Group by date and energy type, and aggregate energy used
    #     data = consumptions.annotate(
    #         date=TruncDate('create_time')
    #     ).values('date', 'energy_type').annotate(
    #         daily_energy=Sum('energy_used')
    #     ).order_by('date', 'energy_type')
    #
    #     # Formatting the result as a list of dictionaries
    #     return [{'date': entry['date'], 'energy_type': entry['energy_type'], 'daily_energy': entry['daily_energy']} for
    #             entry in data]

class EnergySource(models.Model):
    parent = models.ForeignKey(
        'self',  # 'self' indicates a ForeignKey relation to the same model
        on_delete=models.SET_NULL,  # What to do if the parent is deleted
        null=True,  # Allows for top-level sources without parents
        blank=True,  # Makes it optional in forms
        related_name='children'  # How to access the children of a parent node
    )
    type = models.CharField(max_length=100, default='default_type')
    supplier = models.CharField(max_length=100, default='default_supplier')
    current_reservation = models.FloatField(default=0.0)
    price = models.FloatField()
    level = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


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
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class EnergyConsumption(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='consumptions')
    in_energysource = models.ForeignKey(EnergySource, on_delete=models.CASCADE, related_name='in_consumptions',default='1')
    in_energy_quantity = models.FloatField(default=0.0)
    out_energysource = models.ForeignKey(EnergySource, on_delete=models.CASCADE, related_name='out_consumptions',default='2')
    out_energy_quantity = models.FloatField(default=0.0)
    energy_used = models.FloatField(default=0.0)  # Default value for 'energy_used'
    cost = models.FloatField(default=0.0)
    expect_used = models.FloatField(default=0.0)  # Default value for 'energy_used'
    expect_cost = models.FloatField(default=0.0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class MaintenanceRecord(models.Model):
    energy_consumption = models.ForeignKey(EnergyConsumption, on_delete=models.CASCADE,default=1)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records')
    operator = models.CharField(max_length=100, default='Unknown Operator')  # Default value for 'operator'
    details = models.TextField(default='No details provided.')  # Default value for 'details'
    status = models.CharField(max_length=100, default='Pending')  # Default value for 'status'
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
