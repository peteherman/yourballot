from typing import Any

from rest_framework.response import Response


def ballot_response(result: dict, success: bool = True, errors: list[str] | None = None, **kwargs: Any) -> Response:
    return Response(
        {
            "result_info": {
                "next": None,
                "previous": None,
                "success": success,
                "errors": errors or [],
                "total": 0,
            },
            "result": result,
        },
        **kwargs
    )
