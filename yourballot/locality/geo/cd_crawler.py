from typing import Any
from uuid import uuid4

from yourballot.locality.geo.loader import CongressionalDistrictLoader
from yourballot.locality.geo.models import GeoJsonType, State, StateGeoJson
from yourballot.locality.geo.serializers import StateGeoJsonSerializer
from yourballot.provider.congress_district_geo import CongressionalDistrictGeoJsonProvider


class CongressionalDistrictResponseSerializer:
    @classmethod
    def deserialize(
        cls, data: dict, state_abbreviation: State, name: str | None = None, **kwargs: dict[str, Any]
    ) -> StateGeoJson:
        return StateGeoJson(
            id=str(uuid4()),
            type=GeoJsonType.CONGRESSIONAL_DISTRICT,
            name=name or "",
            data=data,
            state=state_abbreviation,
            opt=kwargs,
        )


class CongressionalDistrictCrawler:

    def __init__(self, state: State) -> None:
        self.state = state
        self.provider = CongressionalDistrictGeoJsonProvider(str(state))
        self.serializer = StateGeoJsonSerializer()
        self.loader = CongressionalDistrictLoader()

    def crawl(self) -> None:
        congressional_district = 1
        transformed_assets: list[StateGeoJson] = []
        while True:
            response = self.provider.get_district_geojson(congressional_district)
            if response:
                opt = {"congressional_district": congressional_district}
                state_geo_model = CongressionalDistrictResponseSerializer.deserialize(
                    response, self.state, name=f"Congressional Distirct {congressional_district}", **opt  # type: ignore
                )
                transformed_assets.append(state_geo_model)

                congressional_district += 1
            else:
                break

        for transformed_asset in transformed_assets:
            self.loader.save(transformed_asset)
