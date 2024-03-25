from dataclasses import dataclass
from functools import cached_property
from typing import Any, cast


@dataclass
class Point:
    x: float
    y: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        return False


@dataclass
class Side:
    start: Point
    end: Point

    @cached_property
    def slope(self) -> float | None:
        run = self.end.x - self.start.x
        if run == 0:
            return None
        rise = self.end.y - self.start.y
        return rise / run

    @cached_property
    def y_intercept(self) -> float | None:
        return self.start.y - (self.slope * self.start.x) if self.slope is not None else None

    def intersects(self, other: "Side") -> Point | None:
        # If parallel, don't intersect
        if self.slope == other.slope:
            return None

        # One of slopes is undefined
        # line one: y = mx + b1
        # line two: x = b2
        # x_intersect = b2
        # y = m(b2) = b1
        if self.slope is None or other.slope is None:
            line_one = self if self.slope is not None else other
            line_two = self if line_one != self else other
            x_intersect = line_two.start.x
            y_intersect = line_one.slope * x_intersect + line_one.y_intercept  # type: ignore
            possible_intersect = Point(x_intersect, y_intersect)
            if line_one.point_within_bounds(possible_intersect) and line_two.point_within_bounds(possible_intersect):
                return possible_intersect
            return None

        # Both have defined slope
        # line one: y = m1x + b1
        # line two: y = m2x + b2
        # m1x + b1 = m2x + b2
        # (m1 - m2)x = (b2 - b1)
        # x = (b2 - b1) / (m1 - m2)
        x_intersect = (other.y_intercept - self.y_intercept) / (self.slope - other.slope)  # type: ignore
        y_intersect = self.slope * x_intersect + self.y_intercept  # type: ignore
        possible_intersect = Point(x_intersect, y_intersect)
        if self.point_within_bounds(possible_intersect) and other.point_within_bounds(possible_intersect):
            return possible_intersect
        return None

    def point_within_bounds(self, point: Point) -> bool:
        x_in_bounds = point.x >= self.start.x and point.x <= self.end.x
        y_in_bounds = (
            point.y >= self.start.y and point.y <= self.end.y
            if self.slope is None or self.slope >= 0
            else point.y <= self.start.y and point.y >= self.end.y
        )
        return x_in_bounds and y_in_bounds


@dataclass
class Polygon:
    sides: list[Side]

    @classmethod
    def from_geojson(cls, jsondata: dict[str, Any]) -> "Polygon":
        assert jsondata.get("type") == "Polygon"
        coordinates = jsondata.get("coordinates", [])
        assert len(coordinates) == 1
        assert len(coordinates[0]) >= 3
        coordinates = coordinates[0]

        last_point: Point | None = None
        first_point: Point | None = None
        sides = []
        for coordinate in coordinates:
            new_point = Point(*coordinate)
            if last_point:
                sides.append(Side(last_point, new_point))
            else:
                first_point = new_point
            last_point = new_point

        last_point = cast(Point, last_point)
        first_point = cast(Point, first_point)
        sides.append(Side(last_point, first_point))
        return Polygon(sides=sides)

    def point_is_inside(self, point: Point) -> bool:
        x, y = point.x, point.y
        inside = False

        # Loop through each edge of the polygon
        for side in self.sides:
            if (side.start.y > y) != (side.end.y > y) and x < side.start.x + (side.end.x - side.start.x) * (
                y - side.start.y
            ) / (side.end.y - side.start.y):
                inside = not inside

        return inside
