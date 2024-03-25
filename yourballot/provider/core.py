from enum import StrEnum
from typing import Any

from requests import Request, Response, Session


class HttpMethod(StrEnum):
    GET = "GET"


class HttpProvider:

    def __init__(self, session: Session):
        self.session = session

    def http_ok(self, response: Response) -> bool:
        return response.status_code >= 200 and response.status_code < 300

    def execute_request(
        self,
        url: str,
        method: HttpMethod = HttpMethod.GET,
        headers: dict[str, Any] = {},
        data: Any | None = None,
        params: dict[str, Any] = {},
    ) -> Response:

        request = Request(method.value, url, data=data, headers=headers, params=params)
        prepped_request = self.session.prepare_request(request)
        return self.session.send(prepped_request)
