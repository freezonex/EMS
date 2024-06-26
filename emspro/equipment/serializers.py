from rest_framework import serializers
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

class WorkshopListRequestSerializer(serializers.Serializer):
    workshop_id = serializers.IntegerField(required=False)
    workshop_name = serializers.CharField(required=False)
    page_number = serializers.IntegerField(required=True)
    page_size = serializers.IntegerField(required=True)



class WorkshopEnergySerializer(serializers.Serializer):
    name = serializers.CharField()
    total_energy_used = serializers.FloatField()

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class EnergyConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyConsumption
        fields = '__all__'

class EquipmentEnergySerializer(serializers.Serializer):
    name = serializers.CharField()
    energy_used = serializers.FloatField()

class EnergyBalanceSerializer(serializers.Serializer):
    actually_used = serializers.FloatField()
    energy_used = serializers.FloatField()
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class EnergySourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergySource
        fields = '__all__'


class EnergyTypeUsageSerializer(serializers.Serializer):
    energy_type = serializers.CharField()
    percentage = serializers.FloatField()

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'