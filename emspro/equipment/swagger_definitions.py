# swagger_definitions.py
from drf_yasg import openapi



workshop_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'workshop_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the workshop'),
        'workshop_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the workshop'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10),
    }
)

equipment_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'equipment_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the equipment'),
        'equipment_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the equipment'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10),
    }
)

energysource_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'source_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the energysource'),
        'source_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the energysource'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10),
    }
)

energyconsumption_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'consumption_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the energyconsumption'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10)
    }
)

energyplan_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'plan_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the energyplan'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10)
    }
)



maintenance_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'maintenance_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the maintanence'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10)
    }
)

alarm_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'alarm_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the alarm'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10)
    }
)