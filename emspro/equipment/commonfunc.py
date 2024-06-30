
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage

class StandardResultsSetPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        """Custom pagination to manually handle pagination based on POST data."""
        page_size = request.data.get('page_size', self.page_size)  # Default page size from POST or use default
        page_number = request.data.get('page_number', 1)  # Default page number from POST or 1

        paginator = Paginator(queryset, page_size)
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            return None  # Handle empty page scenario, possibly return an empty list or custom response

        self.page = page
        self.request = request
        return list(page)

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
