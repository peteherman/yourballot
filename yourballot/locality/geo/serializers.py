from abc import ABC, abstractmethod
from json import loads as json_loads
from typing import cast

from yourballot.locality.geo.models import FederalGeoJson, GeoJson, GeoJsonType, State, StateGeoJson


class GeoJsonSerializerBase(ABC):

    @abstractmethod
    @classmethod
    def serialize(cls, model: GeoJson) -> dict:
        pass

    @abstractmethod
    @classmethod
    def deserialize(cls, data: str) -> GeoJson:
        pass


class FederalGeoJsonSerializer(GeoJsonSerializerBase):

    @classmethod
    def serializer(cls, model: FederalGeoJson) -> dict:
        return {"id": str(model.id), "type": str(model.type), "name": str(model.name) or None, "data": model.data}

    @classmethod
    def deserialize(cls, model_data: str) -> FederalGeoJson:
        model_data: dict = dict(json_loads(model_data))
        id: str | None = model_data.get("id")
        assert id is not None
        type: str | None = model_data.get("type")
        assert type is not None
        type: GeoJsonType = GeoJsonType[type]
        name: str | None = model_data.get("name")
        name = cast(str, name)
        data: dict | None = model_data.get("data")
        data = cast(dict, data)

        return FederalGeoJson(id=id, type=type, name=name, data=data)


class StateGeoJsonSerializer(GeoJsonSerializerBase):

    @classmethod
    def serializer(cls, model: StateGeoJson) -> dict:
        return {
            "id": str(model.id),
            "type": str(model.type),
            "name": str(model.name) or None,
            "data": model.data,
            "state": str(model.state),
        }

    @classmethod
    def deserialize(cls, model_data: str) -> StateGeoJson:
        model_data: dict = dict(json_loads(model_data))
        id: str | None = model_data.get("id")
        assert id is not None
        type: str | None = model_data.get("type")
        assert type is not None
        type: GeoJsonType = GeoJsonType[type]
        name: str | None = model_data.get("name")
        name = cast(str, name)
        data: dict | None = model_data.get("data")
        data = cast(dict, data)
        state: str | None = model_data.get("state")
        assert state is not None
        state: State = State[state]

        return StateGeoJson(id=id, type=type, name=name, data=data, state=state)
