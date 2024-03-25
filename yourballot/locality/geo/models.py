from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4


class GeoJsonType(StrEnum):
    CONGRESS_DISTRICT = "Congressional District"


class State(StrEnum):
    NY = "New York"


@dataclass
class GeoJson:
    type: GeoJsonType
    name: str | None
    data: dict


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
