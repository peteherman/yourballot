from rest_framework import pagination
from rest_framework.response import Response


class CustomPageBasedPagination(pagination.PageNumberPagination):
    """
    Custom pagination class, uses page based pagination
    """

    def get_paginated_response(self, data: list | dict) -> Response:
        return Response(
            {
                "result_info": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "total": self.page.paginator.count,  # type: ignore
                },
                "result": data,
            }
        )
