from abc import ABC
from json import dump as json_dump
from os import mkdir as os_mkdir
from os import path as os_path
from typing import TypeVar
from uuid import UUID

from django.utils.functional import classproperty

from yourballot.locality.geo.models import CongressionalDistrict, IDBoundGeoJson, Zipcode
from yourballot.locality.geo.serializers import GeoJsonSerializerBase, StateGeoJsonSerializer, ZipcodeGeoJsonSerializer

GeoModel = TypeVar("GeoModel", bound=IDBoundGeoJson)


class GeoLoaderBase(ABC):
    base_path: str = os_path.join(os_path.dirname(__file__), "geojson")
    serializer_class: type[GeoJsonSerializerBase]
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
        if hasattr(cls.model_class, "Meta") and hasattr(cls.model_class.Meta, "folder_name"):
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
    def load(cls, id: str | UUID) -> IDBoundGeoJson:
        with open(cls.get_file_path_from_id(id), "r") as fh:
            raw_data = fh.read()
            deserialized_data = cls.serializer_class.deserialize(raw_data)
            return deserialized_data


class CongressionalDistrictLoader(GeoLoaderBase):
    serializer_class = StateGeoJsonSerializer
    model_class = CongressionalDistrict

    @classproperty
    def base_path(cls) -> str:  # type: ignore
        return os_path.join(GeoLoaderBase.base_path, "state")


class ZipcodeLoader(GeoLoaderBase):
    serializer_class = ZipcodeGeoJsonSerializer
    model_class = Zipcode

    @classproperty
    def base_path(cls) -> str:  # type: ignore
        return os_path.join(GeoLoaderBase.base_path, "zipcode")
