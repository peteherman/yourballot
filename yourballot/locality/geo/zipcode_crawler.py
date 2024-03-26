from yourballot.locality.geo.loader import ZipcodeLoader
from yourballot.locality.geo.serializers import ZipcodeFromUSShapefileSerializer
from yourballot.locality.geo.shapefile import convert_shapefile_to_geojson_objects


class ZipcodeCrawler:

    def __init__(self, zipcode_shapefile_path: str) -> None:
        self.file_path = zipcode_shapefile_path
        self.serializer = ZipcodeFromUSShapefileSerializer()
        self.loader = ZipcodeLoader()

    def crawl(self) -> None:
        geojson_objects = convert_shapefile_to_geojson_objects(self.file_path)
        for geojson_object in geojson_objects:
            zipcode_model = self.serializer.deserialize(geojson_object)
            self.loader.save(zipcode_model)
