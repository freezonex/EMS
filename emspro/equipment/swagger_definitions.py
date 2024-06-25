# swagger_definitions.py
from drf_yasg import openapi



workshop_list_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['page_number', 'page_size'],  # List required fields here
    properties={
        'workshop_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the workshop'),
        'workshop_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the workshop'),
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number',default=1),
        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of items per page',default=10),
    }
)