from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import DateFilter, DateTimeFromToRangeFilter
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord
from .serializers import WorkshopSerializer, EquipmentSerializer,EnergyConsumptionSerializer,EnergySourceSerializer,MaintenanceRecordSerializer

class WorkshopFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = Workshop
        fields = {
            'name': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
        }

class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WorkshopFilter

    @action(detail=True, methods=['get'])
    def total_energy_consumption(self, request, pk=None):
        workshop = self.get_object()
        total_consumption = workshop.total_energy_consumption()
        return Response({'total_energy_consumption': total_consumption})

    @action(detail=True, methods=['post'])
    def oneday_energy_consumption(self, request, pk=None):
        workshop = self.get_object()
        date_input = request.data.get('date')  # expecting date in 'YYYY-MM-DD' format
        date = parse_date(date_input)
        energy_type = request.data.get('energy_type', None)  # Defaults to None if not provided
        if date is None:
            return Response({'error': 'Invalid date format'}, status=400)
        daily_consumption = workshop.Oneday_energy_consumption(date=date,energy_type=energy_type)
        return Response({'date': date.isoformat(), 'daily_energy_consumption': daily_consumption})

    @action(detail=False, methods=['post'], url_path='daily_energy_consumption')
    def get_workshop_daily_consumption(self, request):
        workshop_id = request.data.get('workshop_id')
        if not workshop_id:
            return Response({"error": "workshop_id is required"}, status=400)

        try:
            workshop = Workshop.objects.get(id=workshop_id)
        except Workshop.DoesNotExist:
            return Response({"error": "Workshop not found"}, status=404)

        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        energy_type = request.data.get('energy_type', None)

        data = workshop.daily_energy_consumption(start_date=start_date, end_date=end_date, energy_type=energy_type)

        return Response(data)


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
            'volume': ['exact', 'icontains'],
            'electric': ['exact', 'icontains'],
            'pressure': ['exact', 'icontains'],
            'temperature': ['exact', 'icontains'],
            'actual_rate': ['exact', 'icontains'],
            'standard_rate': ['exact', 'icontains'],
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
            'energy_type': ['exact'],
            'energysource': ['exact'],
            'energy_used': ['exact', 'icontains'],
            'cost': ['exact', 'icontains'],
            'expect_cost': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
        }



class EnergyConsumptionViewSet(viewsets.ModelViewSet):
    queryset = EnergyConsumption.objects.all()
    serializer_class = EnergyConsumptionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergyConsumptionFilter

    def perform_create(self, serializer):
        energy_source = serializer.validated_data['energysource']
        equipment = serializer.validated_data['equipment']
        energy_type = energy_source.type
        energy_used = serializer.validated_data['energy_used']
        expect_used = equipment.standard_rate
        rounded_expect_used = round(expect_used, 8)
        cost = energy_used * energy_source.price
        expect_cost = equipment.standard_rate * energy_source.price
        rounded_cost = round(cost, 8)
        rounded_expect_cost = round(expect_cost, 8)
        # Pass the calculated cost to the serializer's save method
        serializer.save(energy_type=energy_type)
        serializer.save(cost=rounded_cost)
        serializer.save(expect_cost=rounded_expect_cost)
        serializer.save(expect_used=rounded_expect_used)


class EnergySourceFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergySource
        fields =  {
            'type': ['exact'],
            'supplier': ['exact'],
            'price': ['exact'],
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
            'operator': ['exact'],
            'equipment': ['exact'],
            'create_time': [],
            'update_time': [],
        }

class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceRecordFilter

