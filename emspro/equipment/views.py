from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import DateFilter, DateTimeFromToRangeFilter
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from .models import Workshop, Equipment,EnergyConsumption,EnergySource,MaintenanceRecord
from .serializers import WorkshopSerializer, EquipmentSerializer,EnergyConsumptionSerializer,EnergySourceSerializer,MaintenanceRecordSerializer,EquipmentEnergySerializer,WorkshopEnergySerializer,EnergyTypeUsageSerializer
from django.db import transaction,models
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

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

    @action(detail=True, methods=['get'])
    def total_expected_energy_consumption(self, request, pk=None):
        workshop = self.get_object()
        total_expected_energy_consumption = workshop.total_expected_energy_consumption()
        return Response({'total_expected_energy_consumption': total_expected_energy_consumption})

    @action(detail=False, methods=['get'], url_path='workshop_top_energy_used')
    def top_energy_used(self, request):
        # Calculate the time one day ago from now
        time_threshold = timezone.now() - timedelta(days=1)

        # Query the database for the total energy used by each workshop in the last day
        top_workshops = EnergyConsumption.objects.filter(
            equipment__workshop__isnull=False,
            create_time__gte=time_threshold
        ).values('equipment__workshop__name') \
                            .annotate(total_energy_used=models.Sum('energy_used')) \
                            .order_by('-total_energy_used')[:5]

        # Adjusted list comprehension to properly rename keys
        formatted_equipments = [
            {'name': entry['equipment__workshop__name'], 'total_energy_used': entry['total_energy_used']}
            for entry in top_workshops
        ]

        # Serialize the data
        serializer = WorkshopEnergySerializer(formatted_equipments, many=True)

        # Return the serialized data
        return Response(serializer.data)

    # @action(detail=True, methods=['post'])
    # def oneday_energy_consumption(self, request, pk=None):
    #     workshop = self.get_object()
    #     date_input = request.data.get('date')  # expecting date in 'YYYY-MM-DD' format
    #     date = parse_date(date_input)
    #     energy_type = request.data.get('energy_type', None)  # Defaults to None if not provided
    #     if date is None:
    #         return Response({'error': 'Invalid date format'}, status=400)
    #     daily_consumption = workshop.Oneday_energy_consumption(date=date,energy_type=energy_type)
    #     return Response({'date': date.isoformat(), 'daily_energy_consumption': daily_consumption})
    #
    # @action(detail=False, methods=['post'], url_path='daily_energy_consumption')
    # def get_workshop_daily_consumption(self, request):
    #     workshop_id = request.data.get('workshop_id')
    #     if not workshop_id:
    #         return Response({"error": "workshop_id is required"}, status=400)
    #
    #     try:
    #         workshop = Workshop.objects.get(id=workshop_id)
    #     except Workshop.DoesNotExist:
    #         return Response({"error": "Workshop not found"}, status=404)
    #
    #     start_date = request.data.get('start_date', None)
    #     end_date = request.data.get('end_date', None)
    #     energy_type = request.data.get('energy_type', None)
    #
    #     data = workshop.daily_energy_consumption(start_date=start_date, end_date=end_date, energy_type=energy_type)
    #
    #     return Response(data)


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

    @action(detail=False, methods=['get'], url_path='top_energy_used')
    def top_energy_used(self, request):
        # Calculate the time 30 minutes ago from now
        time_threshold = timezone.now() - timedelta(minutes=3000)

        # Query the database for the top 10 individual records of equipment based on the highest energy used in the last 30 minutes
        top_equipments = EnergyConsumption.objects.filter(create_time__gte=time_threshold) \
                             .order_by('-energy_used')[:10] \
            .values('equipment__name', 'energy_used')  # Ensures the values align with serializer fields

        # Adjust the dictionary keys to match the serializer expectation
        formatted_equipments = [
            {'name': entry['equipment__name'], 'energy_used': entry['energy_used']}
            for entry in top_equipments
        ]

        # Serialize the data
        serializer = EquipmentEnergySerializer(formatted_equipments, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

class EnergyConsumptionFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()
    update_time = DateTimeFromToRangeFilter()
    class Meta:
        model = EnergyConsumption
        fields ={
            'equipment': ['exact'],
            'in_energysource': ['exact'],
            'in_energy_quantity': ['exact'],
            'out_energysource': ['exact'],
            'out_energy_quantity': ['exact'],
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
        with transaction.atomic():  # Ensures atomicity of the operation
            in_energysource = serializer.validated_data['in_energysource']
            out_energysource = serializer.validated_data['out_energysource']
            equipment = serializer.validated_data['equipment']

            in_energy_used = serializer.validated_data['in_energy_quantity']
            out_energy_generated = serializer.validated_data['out_energy_quantity']

            if in_energy_used-out_energy_generated <0:
                raise ValidationError({
                    "detail": "The input energy source must be lager."
                })

            energy_used = in_energy_used-out_energy_generated

            # Check if in_energysource is the parent of out_energysource
            if out_energysource.parent_id != in_energysource.id:
                raise ValidationError({
                    "detail": "The input energy source must be the parent of the output energy source."
                })

            # Calculate costs
            cost = energy_used * in_energysource.price
            expect_used = equipment.standard_rate
            expect_cost = equipment.standard_rate * in_energysource.price

            # Perform rounding
            rounded_in_cost = round(cost, 8)
            rounded_expect_cost = round(expect_cost, 8)
            rounded_expect_used = round(expect_used, 8)

            # Update EnergySource reservations
            in_energysource.current_reservation -= in_energy_used
            out_energysource.current_reservation += out_energy_generated
            in_energysource.save()
            out_energysource.save()

            # Saving the EnergyConsumption instance with calculated fields
            energy_consumption = serializer.save(
                energy_used = energy_used,
                cost=rounded_in_cost,
                expect_cost=rounded_expect_cost,
                expect_used=rounded_expect_used
            )

            if energy_used > (1.30 * expect_used):
                MaintenanceRecord.objects.create(
                    equipment=equipment,
                    operator="default",
                    details="Exceeded expected energy use by 30% or more",
                    status="abnormal",
                    energy_consumption=energy_consumption
                )

    @action(detail=False, methods=['post'], url_path='energy_source_buying')
    def energy_source_buying(self, request):
        # Expecting 'source_id' and 'additional_reserve' in the request data
        source_id = request.data.get('energysource_id')
        additional_reserve = request.data.get('additional_reserve', 0)

        try:
            additional_reserve = float(additional_reserve)  # Convert additional_reserve to float
            with transaction.atomic():
                # Fetch the energy source and update its current reservation
                energy_source = EnergySource.objects.get(id=source_id)
                new_reservation = energy_source.current_reservation + additional_reserve

                # Check if the new reservation would be negative
                if new_reservation < 0:
                    return Response({"error": "Operation would result in negative reserves, which is not allowed."},
                                    status=status.HTTP_400_BAD_REQUEST)

                energy_source.current_reservation = new_reservation
                energy_source.save()

            return Response({"message": "Energy source reservation successfully updated.",
                             "current_reservation": energy_source.current_reservation}, status=status.HTTP_200_OK)

        except EnergySource.DoesNotExist:
            return Response({"error": "Energy source not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid input. Please ensure all values are numerical."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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
            'create_time': [],
            'update_time': [],
        }



class EnergySourceViewSet(viewsets.ModelViewSet):
    queryset = EnergySource.objects.all()
    serializer_class = EnergySourceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EnergySourceFilter
    @action(detail=False, methods=['get'], url_path='energy_usage_percentage')
    def energy_usage_percentage(self, request):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now()

        usage_data = EnergyConsumption.objects.filter(
            create_time__range=(today_start, today_end),
            in_energysource__level=1
        ).values('in_energysource__type') \
            .annotate(total_energy=models.Sum('energy_used')) \
            .order_by('-total_energy')

        total_energy_used_today = sum(item['total_energy'] for item in usage_data)

        percentage_data = [
            {
                'energy_type': item['in_energysource__type'],
                'percentage': (
                            item['total_energy'] / total_energy_used_today * 100) if total_energy_used_today > 0 else 0
            }
            for item in usage_data
        ]

        serializer = EnergyTypeUsageSerializer(percentage_data, many=True)
        return Response(serializer.data)

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

