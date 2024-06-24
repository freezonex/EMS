from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import DateFilter, DateTimeFromToRangeFilter
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord
from .serializers import WorkshopSerializer, EquipmentSerializer,EnergyConsumptionSerializer,EnergySourceSerializer,MaintenanceRecordSerializer,EquipmentEnergySerializer,WorkshopEnergySerializer,EnergyTypeUsageSerializer,EnergyBalanceSerializer

class WorkshopFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = Workshop
        fields = {
            'name': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
        }

class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WorkshopFilter



class EquipmentFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = Equipment
        fields ={
            'name': ['exact', 'icontains'],
            'workshop': ['exact'],
            'type': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'energy_type': ['exact', 'icontains'],
            'volume': ['exact'],
            'electric': ['exact'],
            'pressure': ['exact'],
            'temperature': ['exact'],
            'actual_rate': ['exact'],
            'standard_rate': ['exact'],
            'url': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
        }

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EquipmentFilter


class EnergyConsumptionFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergyConsumption
        fields ={
            'equipment': ['exact'],
            'in_energysource': ['exact'],
            'in_energy_quantity': ['exact'],
            'energy_used': ['exact'],
            'expect_use': ['exact'],
            'cost': ['exact'],
            'expect_cost': ['exact'],
            'energy_loss': ['exact'],
            'create_time': [],
            'update_time': [],
        }



class EnergyConsumptionViewSet(viewsets.ModelViewSet):
    queryset = EnergyConsumption.objects.all()
    serializer_class = EnergyConsumptionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergyConsumptionFilter





class EnergySourceFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergySource
        fields =  {
            'type': ['exact'],
            'supplier': ['exact'],
            'price': ['exact'],
            'current_reservation': ['exact'],
            'energy_code': ['exact'],
            'coal_discount_factor': ['exact'],
            'carbon_emission_factor': ['exact'],
            'unit': ['exact','icontains'],
            'description': ['exact','icontains'],
            'create_user': ['exact','icontains'],
            'create_time': [],
            'update_time': [],
        }



class EnergySourceViewSet(viewsets.ModelViewSet):
    queryset = EnergySource.objects.all()
    serializer_class = EnergySourceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergySourceFilter


class MaintenanceRecordFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = MaintenanceRecord
        fields = {
            'status': ['exact'],
            'operator': ['exact','icontains'],
            'equipment': ['exact'],
            'details': ['exact','icontains'],
            'maintenance_type': ['exact', 'icontains'],
            'scheduled_date': ['exact'],
            'create_time': [],
            'update_time': [],
        }

class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceRecordFilter

