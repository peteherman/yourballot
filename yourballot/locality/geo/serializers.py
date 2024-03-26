from abc import ABC, abstractmethod
from json import loads as json_loads
from typing import TypeVar, cast

from yourballot.locality.geo.models import FederalGeoJson, GeoJson, GeoJsonType, IDBoundGeoJson, State, StateGeoJson

GeoModel = TypeVar("GeoModel", bound=IDBoundGeoJson)


class GeoJsonSerializerBase(ABC):

    @classmethod
    @abstractmethod
    def serialize(cls, model: IDBoundGeoJson) -> dict:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> IDBoundGeoJson:
        pass


class FederalGeoJsonSerializer(GeoJsonSerializerBase):

    @classmethod
    def serialize(cls, model: GeoModel) -> dict:
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
        opt: dict | None = model_data.get("opt")

        return FederalGeoJson(id=id, type=type, name=name, data=data, opt=opt)


class StateGeoJsonSerializer(GeoJsonSerializerBase):

    @classmethod
    def serialize(cls, model: StateGeoJson) -> dict:  # type: ignore
        return {
            "id": str(model.id),
            "type": str(model.type),
            "name": str(model.name) or None,
            "data": model.data,
            "state": str(model.state),
            "opt": model.opt,
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
        opt: dict | None = model_data.get("opt")

        return StateGeoJson(id=id, type=type, name=name, data=data, state=state, opt=opt)