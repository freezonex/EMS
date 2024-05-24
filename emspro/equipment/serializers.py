from rest_framework import serializers
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


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



class EnergySourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergySource
        fields = '__all__'

    def validate(self, data):
        # Check if the level of the energy source is 2 or 3 and require a parent
        if data.get('level') in [2, 3] and not data.get('parent'):
            raise serializers.ValidationError("Parent ID is required for level 2 and 3 energy sources.")
        return data



class EnergyTypeUsageSerializer(serializers.Serializer):
    energy_type = serializers.CharField()
    percentage = serializers.FloatField()

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'