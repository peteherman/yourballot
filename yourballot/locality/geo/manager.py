from abc import ABC
from json import dump as json_dump
from os import path as os_path
from os import walk as os_walk
from typing import Any, Generic, TypeVar
from uuid import UUID

from django.utils.functional import classproperty

from yourballot.locality.geo.models import FederalGeoJson, IDBoundGeoJson, State, StateGeoJson
from yourballot.locality.geo.serializers import FederalGeoJsonSerializer, GeoJsonSerializerBase, StateGeoJsonSerializer

T = TypeVar("T", bound=IDBoundGeoJson)


class ModelNotFoundException(Exception):
    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.message = message
        super().__init__(*args, **kwargs)


class GeoJsonManagerBase(ABC, Generic[T]):
    base_dir: str = os_path.join(os_path.dirname(__file__), "geojson")
    serializer_class: type[GeoJsonSerializerBase]

    @classmethod
    def save(cls, geojson: T) -> None:
        with open(cls.file_path(str(geojson.id)), "w+") as fh:
            serialized_data = cls.serializer_class.serialize(geojson)
            json_dump(serialized_data, fh)

    @classmethod
    def get(cls, id: str | UUID) -> T:
        with open(cls.file_path(str(id)), "r") as fh:
            deserialized_model = cls.serializer_class.deserialize(fh.read())
            return deserialized_model  # type: ignore

    @classmethod
    def file_path(cls, id: str) -> str:
        return os_path.join(cls.base_dir, f"{id}.json")


class FederalGeoJsonManager(GeoJsonManagerBase[FederalGeoJson]):
    serializer_class = FederalGeoJsonSerializer

    @classproperty
    def base_dir(cls) -> str:  # type: ignore
        return os_path.join(super().base_dir, "federal")


class StateGeoJsonManager(GeoJsonManagerBase[StateGeoJson]):
    serializer_class = StateGeoJsonSerializer

    @classproperty
    def base_dir(cls) -> str:  # type: ignore
        return os_path.join(super().base_dir, "state")

    @classmethod
    def file_path_from_model(cls, model: StateGeoJson) -> str:
        return os_path.join(cls.base_dir, str(model.state), f"{id}.json")

    @classmethod
    def save(cls, geojson: StateGeoJson) -> None:
        with open(cls.file_path_from_model(geojson), "w+") as fh:
            serialized_data = cls.serializer_class.serialize(geojson)
            json_dump(serialized_data, fh)

    @classmethod
    def get(cls, id: str | UUID, state: State | None) -> StateGeoJson:  # type: ignore
        if state:
            filepath = os_path.join(cls.base_dir, str(state), f"{str(id)}.json")
            with open(filepath, "r") as fh:
                deserialized_model = cls.serializer_class.deserialize(fh.read())
                return deserialized_model

        for root, _, files in os_walk(cls.base_dir):
            for fname in files:
                filename, _ = os_path.splitext(fname)
                if filename == f"{str(id)}":
                    filepath = os_path.join(root, fname)
                    with open(filepath, "r") as fh:
                        deserialized_model = cls.serializer_class.deserialize(fh.read())
                        return deserialized_model
        raise ModelNotFoundException(f"Unable to locate model with id: {str(id)}")
