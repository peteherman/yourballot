from yourballot.provider.congress_district_geo import CongressionalDistrictGeoJsonProvider


class CongressionalDistrictCrawler:

    def __init__(self, state_abbreviation: str) -> None:
        self.provider = CongressionalDistrictGeoJsonProvider(state_abbreviation)

    def crawl(self) -> None:
        pass
