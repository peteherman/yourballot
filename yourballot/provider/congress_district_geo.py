from typing import cast

from requests import Session
from rest_framework import status

from yourballot.provider.core import HttpMethod, HttpProvider


class CongressionalDistrictGeoJsonProvider(HttpProvider):
    base_url: str = "https://theunitedstates.io/districts/cds/2012/"  # NY-1/shape.geojson

    def __init__(self, state_abbreviation: str) -> None:
        self.state_abbreviation = state_abbreviation

        super().__init__(Session())

    def get_district_geojson(self, district_number: int) -> dict | None:

        url = f"{self.base_url}{self.state_abbreviation}-{district_number}/shape.geojson"
        response = self.execute_request(url=url, method=HttpMethod.GET)
        if self.http_ok(response):
            return dict(response.json())

        if response.status_code == status.HTTP_404_NOT_FOUND:
            return None

        raise Exception("Unexpected status code and response: ", response)
