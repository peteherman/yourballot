from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4


class GeoJsonType(StrEnum):
    CONGRESSIONAL_DISTRICT = "Congressional District"


class State(StrEnum):
    NY = "NY"


@dataclass
class GeoJson:
    type: GeoJsonType
    name: str | None
    data: dict
    opt: dict | None


@dataclass
class IDMixin:
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class IDBoundGeoJson(IDMixin, GeoJson):
    pass


@dataclass
class FederalGeoJson(IDBoundGeoJson):
    pass


@dataclass
class StateMixin:
    state: State


@dataclass
class StateGeoJson(IDBoundGeoJson, StateMixin):
    pass


@dataclass
class CongressionalDistrict(IDBoundGeoJson, StateMixin):
    class Meta:
        folder_name = "congressional_district"
