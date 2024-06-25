from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import DateFilter, DateTimeFromToRangeFilter
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord
from .serializers import WorkshopSerializer, EquipmentSerializer,EnergyConsumptionSerializer,EnergySourceSerializer,MaintenanceRecordSerializer,EquipmentEnergySerializer,WorkshopListRequestSerializer,EnergyTypeUsageSerializer,EnergyBalanceSerializer
from rest_framework.pagination import PageNumberPagination
from .swagger_definitions import workshop_list_params
from drf_yasg.utils import swagger_auto_schema
class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page_number'

    def get_paginated_response(self, data):
        return Response({
            'code': 200,
            'message': 'Success',
            'data': {
                'list': data,
                'pageNum': self.page.number,
                'pageSize': self.page.paginator.per_page,
                'total': self.page.paginator.count,
                'totalPage': self.page.paginator.num_pages,
            }
        })


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
            page_number = serializer.validated_data.get('page_number', 1)
            page_size = serializer.validated_data.get('page_size', 10)

            # Filter by optional fields if provided
            filters = {}
            if 'workshop_id' in serializer.validated_data:
                filters['id'] = serializer.validated_data['workshop_id']
            if 'workshop_name' in serializer.validated_data:
                filters['name__icontains'] = serializer.validated_data['workshop_name']

            queryset = self.filter_queryset(self.get_queryset().filter(**filters))
            paginator = StandardResultsSetPagination()
            paginator.page_size = page_size
            page = paginator.paginate_queryset(queryset, request)

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
            'in_energy_source': ['exact'],
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

