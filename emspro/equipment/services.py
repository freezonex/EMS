# services.py

from django.db.models import Sum
from .models import Workshop, Equipment

def calculate_total_workshop_energy(workshop_id):
    workshop = Workshop.objects.get(pk=workshop_id)
    total_energy = Equipment.objects.filter(workshop=workshop).aggregate(
        total_energy=Sum('consumptions__energy_used')
    )['total_energy']
    return total_energy

def calculate_total_energy_cost(workshop_id):
    workshop = Workshop.objects.get(pk=workshop_id)
    total_cost = 0
    for equipment in workshop.equipment.all():
        for consumption in equipment.consumptions.all():
            total_cost += consumption.energy_used * consumption.energysource.price
    return total_cost
