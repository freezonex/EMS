from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import DateFilter, DateTimeFromToRangeFilter
from rest_framework import viewsets, status
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord,AlarmRecord,EnergyPlan
from .serializers import WorkshopSerializer, EquipmentSerializer,EnergyConsumptionSerializer,EnergySourceSerializer,MaintenanceRecordSerializer,EquipmentEnergySerializer,WorkshopListRequestSerializer,EnergyTypeUsageSerializer,EnergyBalanceSerializer,EnergyPlanSerializer,AlarmRecordSerializer,EquipmentListRequestSerializer,EnergySourceListRequestSerializer
from .swagger_definitions import workshop_list_params,equipment_list_params,energysource_list_params
from drf_yasg.utils import swagger_auto_schema
from .commonfunc import StandardResultsSetPagination


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
            'deleted':[]
        }


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WorkshopFilter
    pagination_class = StandardResultsSetPagination

    @action(methods=['post'], detail=False,url_path='workshopList')
    @swagger_auto_schema(
        request_body=workshop_list_params,
        responses={200: WorkshopSerializer(many=True)},
        operation_description="Post list of workshops with pagination"
    )
    def post_list(self, request):
        serializer = WorkshopListRequestSerializer(data=request.data)
        if serializer.is_valid():
            queryset = self.get_queryset().filter(deleted=0)
            filter_kwargs = {}
            if 'workshop_id' in serializer.validated_data:
                filter_kwargs['workshop_id'] = serializer.validated_data['workshop_id']
            if 'workshop_name' in serializer.validated_data:
                filter_kwargs['name__icontains'] = serializer.validated_data['workshop_name']
            # Use the paginator directly here, relying on it to pull data from POST
            queryset = self.filter_queryset(self.get_queryset().filter(**filter_kwargs))
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request, self)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        return Response({"code": 400, "message": "Invalid data", "data": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True, url_path='delete')
    def soft_delete(self, request, pk=None):
        workshop = self.get_object()
        workshop.deleted = 1
        workshop.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom 'list' action that accepts POST to fetch data


class EquipmentFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = Equipment
        fields ={
            'name': ['exact', 'icontains'],
            'workshop_id': ['exact'],
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
            'deleted': []
        }

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EquipmentFilter
    pagination_class = StandardResultsSetPagination
    @action(methods=['post'], detail=False,url_path='equipmentList')
    @swagger_auto_schema(
        request_body=equipment_list_params,
        responses={200: EquipmentSerializer(many=True)},
        operation_description="Post list of equipment with pagination"
    )
    def post_list(self, request):
        serializer = EquipmentListRequestSerializer(data=request.data)
        if serializer.is_valid():
            queryset = self.get_queryset().filter(deleted=0)
            filter_kwargs = {}
            if 'equipment_id' in serializer.validated_data:
                filter_kwargs['equipment_id'] = serializer.validated_data['equipment_id']
            if 'equipment_name' in serializer.validated_data:
                filter_kwargs['name__icontains'] = serializer.validated_data['equipment_name']
            # Use the paginator directly here, relying on it to pull data from POST
            queryset = self.filter_queryset(self.get_queryset().filter(**filter_kwargs))
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request, self)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        return Response({"code": 400, "message": "Invalid data", "data": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True, url_path='delete')
    def soft_delete(self, request, pk=None):
        equipment = self.get_object()
        equipment.deleted = 1
        equipment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom 'list' action that accepts POST to fetch data




class EnergyConsumptionFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergyConsumption
        fields ={
            'equipment_id': ['exact'],
            'in_energy_source': ['exact'],
            'in_energy_quantity': ['exact'],
            'energy_used': ['exact'],
            'expect_use': ['exact'],
            'cost': ['exact'],
            'expect_cost': ['exact'],
            'energy_loss': ['exact'],
            'create_time': [],
            'update_time': [],
            'deleted': []
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
            'deleted': []
        }



class EnergySourceViewSet(viewsets.ModelViewSet):
    queryset = EnergySource.objects.all()
    serializer_class = EnergySourceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergySourceFilter
    pagination_class = StandardResultsSetPagination
    @action(methods=['post'], detail=False,url_path='energysourceList')
    @swagger_auto_schema(
        request_body=energysource_list_params,
        responses={200: EquipmentSerializer(many=True)},
        operation_description="Post list of energysource with pagination"
    )
    def post_list(self, request):
        serializer = EquipmentListRequestSerializer(data=request.data)
        if serializer.is_valid():
            queryset = self.get_queryset().filter(deleted=0)
            filter_kwargs = {}
            if 'source_id' in serializer.validated_data:
                filter_kwargs['source_id'] = serializer.validated_data['source_id']
            if 'source_name' in serializer.validated_data:
                filter_kwargs['name__icontains'] = serializer.validated_data['source_name']
            # Use the paginator directly here, relying on it to pull data from POST
            queryset = self.filter_queryset(self.get_queryset().filter(**filter_kwargs))
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request, self)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        return Response({"code": 400, "message": "Invalid data", "data": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True, url_path='delete')
    def soft_delete(self, request, pk=None):
        energysource = self.get_object()
        energysource.deleted = 1
        energysource.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom 'list' action that accepts POST to fetch data



class EnergyPlanFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergyPlan
        fields = {
            'source_id': ['exact'],
            'intervals': ['exact'],
            'start_period': ['exact'],
            'end_period': ['exact'],
            'energy_target': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
            'deleted': []
        }

class EnergyPlanViewSet(viewsets.ModelViewSet):
    queryset = EnergyPlan.objects.all()
    serializer_class = EnergyPlanSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergyPlanFilter



class AlarmRecordFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = AlarmRecord
        fields = {
            'equipment_id': ['exact'],
            'consumption_id': ['exact'],
            'details': ['exact','icontains'],
            'maintenance_id': ['exact'],
            'alarm_type': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'create_time': [],
            'update_time': [],
            'deleted': []
        }

class AlarmRecordViewSet(viewsets.ModelViewSet):
    queryset = AlarmRecord.objects.all()
    serializer_class = AlarmRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AlarmRecordFilter



class MaintenanceRecordFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = MaintenanceRecord
        fields = {
            'status': ['exact'],
            'operator': ['exact','icontains'],
            'equipment_id': ['exact'],
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


