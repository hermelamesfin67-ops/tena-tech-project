
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from medicines.models import Drug


class DrugPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"

    def get_paginated_response(self, data):
        total_medicines = Drug.objects.filter(
            is_active=True
        ).count()

        return Response({
            "count": self.page.paginator.count,
            "total_medicines": total_medicines,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"
