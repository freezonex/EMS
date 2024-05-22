from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Workshop, Equipment, EnergyConsumption, EnergySource, MaintenanceRecord

admin.site.register(Workshop)

admin.site.register(Equipment)

admin.site.register(EnergyConsumption)

admin.site.register(EnergySource)

admin.site.register(MaintenanceRecord)
