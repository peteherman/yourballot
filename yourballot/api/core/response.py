from typing import Any

from rest_framework.response import Response


def ballot_response(result: dict, **kwargs: Any) -> Response:
    return Response(
        {
            "result_info": {
                "next": None,
                "previous": None,
                "total": 0,
            },
            "result": result,
        },
        **kwargs
    )
