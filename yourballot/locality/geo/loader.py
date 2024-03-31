from abc import ABC
from json import dump as json_dump
from os import listdir as os_listdir
from os import mkdir as os_mkdir
from os import path as os_path
from typing import Generic, cast
from uuid import UUID

from django.utils.functional import classproperty
from shapely.geometry import shape  # type: ignore

from yourballot.locality.geo.models import CongressionalDistrict, GeoModel, IDBoundGeoJson, Zipcode
from yourballot.locality.geo.serializers import GeoJsonSerializerBase, StateGeoJsonSerializer, ZipcodeGeoJsonSerializer
from yourballot.locality.models.political_locality import PoliticalLocality, PoliticalLocalityType
from yourballot.locality.models.zipcode_locality import ZipcodeLocality


class GeoLoaderBase(ABC, Generic[GeoModel]):
    base_path: str = os_path.join(os_path.dirname(__file__), "geojson")
    serializer_class: type[GeoJsonSerializerBase[GeoModel]]
    model_class: type[IDBoundGeoJson]

    @classmethod
    def get_file_path(cls, model: GeoModel) -> str:
        file_path = cls.base_path
        file_path = cls._add_model_classes_folder_name(file_path)
        if not os_path.exists(file_path):
            os_mkdir(file_path)
        return os_path.join(file_path, f"{model.id}.json")

    @classmethod
    def _add_model_classes_folder_name(cls, file_path: str) -> str:
        if cls.model_class.Meta.folder_name:
            file_path = os_path.join(file_path, cls.model_class.Meta.folder_name)
        return file_path

    @classmethod
    def get_file_path_from_id(cls, id: str | UUID) -> str:
        file_path = cls.base_path
        file_path = cls._add_model_classes_folder_name(file_path)
        return os_path.join(file_path, f"{id}.json")

    @classmethod
    def save(cls, model: GeoModel) -> None:
        with open(cls.get_file_path(model), "w+") as fh:
            serialized_data = cls.serializer_class.serialize(model)
            json_dump(serialized_data, fh)

    @classmethod
    def load(cls, id: str | UUID) -> GeoModel:
        with open(cls.get_file_path_from_id(id), "r") as fh:
            raw_data = fh.read()
            deserialized_data = cls.serializer_class.deserialize(raw_data)
            deserialized_data = cast(GeoModel, deserialized_data)
            return deserialized_data

    @classproperty
    def all_ids(cls) -> list[str]:
        subfolder_name = cls.model_class.Meta.folder_name
        full_path = cls.base_path
        if subfolder_name:
            full_path = os_path.join(full_path, subfolder_name)
        return [os_path.splitext(filename)[0] for filename in os_listdir(full_path)]


class CongressionalDistrictLoader(GeoLoaderBase):
    serializer_class = StateGeoJsonSerializer
    model_class = CongressionalDistrict

    @classproperty
    def base_path(cls) -> str:  # type: ignore
        return os_path.join(GeoLoaderBase.base_path, "state")


def create_congressional_district_localities() -> None:
    """
    Iterates over all congressional districts accessible via the CongressionalDistrictLoader
    and creates django models for the political localities that represent this type
    """

    loader = CongressionalDistrictLoader()
    congressional_district_ids = loader.all_ids
    for cd_id in congressional_district_ids:
        district = loader.load(cd_id)
        if not district.name:
            district.name = "Congressional District"
        district.name = f"{district.state} - {district.name}"
        PoliticalLocality.objects.create(geo_json_id=cd_id, name=district.name, type=PoliticalLocalityType.FEDERAL)


class ZipcodeLoader(GeoLoaderBase):
    serializer_class = ZipcodeGeoJsonSerializer
    model_class = Zipcode

    @classproperty
    def base_path(cls) -> str:  # type: ignore
        return os_path.join(GeoLoaderBase.base_path, "zipcode")


MINIMUM_COVERING_PERCENTAGE = 50.0


def create_zipcode_locality(locality_geo_loader: type[GeoLoaderBase], locality_type: PoliticalLocalityType) -> None:
    """
    Will generate django ZipcodeLocality model records by identifying the zipcode-politicallocalitytype object with the
    largest intersection area
    """
    zipcode_ids = ZipcodeLoader.all_ids
    for zipcode_id in zipcode_ids:
        zipcode = ZipcodeLoader.load(zipcode_id)
        zipcode_shape = shape(zipcode.data)
        largest_covering_area, largest_covering_locality = 0.0, None
        for locality_geo_id in locality_geo_loader.all_ids:
            locality_geo_model = locality_geo_loader.load(locality_geo_id)
            locality_geo_shape = shape(locality_geo_model.data)
            political_locality_model = PoliticalLocality.objects.filter(geo_json_id=locality_geo_id).first()
            if not political_locality_model:
                raise Exception(
                    f"Geo locality with id: {locality_geo_id} does not have a corresponding PoliticalLocality model"
                )
            intersection = locality_geo_shape.intersection(zipcode_shape)
            if intersection.area > largest_covering_area:
                largest_covering_area = intersection.area
                largest_covering_locality = political_locality_model

        percent_zipcode_covered = float(largest_covering_area) / float(zipcode_shape.area) * 100
        if largest_covering_locality and percent_zipcode_covered >= MINIMUM_COVERING_PERCENTAGE:
            ZipcodeLocality.objects.create(zipcode=zipcode.zipcode, political_locality=largest_covering_locality)
