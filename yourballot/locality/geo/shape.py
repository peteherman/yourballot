from copy import deepcopy
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
        return cls.from_coordinate_list(coordinates)

    @classmethod
    def from_coordinate_list(cls, coordinates: list[list[float | int]]) -> "Polygon":
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

    @classmethod
    def from_point_list(cls, points: list[Point]) -> "Polygon":
        last_point: Point | None = None
        first_point: Point | None = None
        sides = []
        for new_point in points:
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

    @cached_property
    def area(self) -> float:
        ## Source: https://web.archive.org/web/20100405070507/http://valis.cs.uiuc.edu/~sariel/research/CG/compgeom/msg00831.html
        area = 0.0
        for side in self.sides:
            area += side.start.x * side.end.y
            area -= side.start.y * side.end.x
        return abs(area / 2)

    def intersection_area(self, other: "Polygon") -> float:
        """
        Attempt at calculating the intersection area via the Sutherland-Hodgman algorithm to identify
        the "clipping area". Derived from: https://github.com/mhdadk/sutherland-hodgman
        """
        output = [p.start for p in self.sides]
        for i in range(len(other.sides)):
            # To save the vertices of the new (clipped) subject polygon
            next_s = deepcopy(output)

            # stores the vertices of the final clipped polygon
            output = []

            # these two vertices define a line segment (edge) in the clipping
            # polygon. It is assumed that indices wrap around, such that if
            # i = 0, then i - 1 = M.
            c_vertex1 = other.sides[i].start
            c_vertex2 = other.sides[i].end
            c_side = Side(c_vertex1, c_vertex2)
            for j in range(len(self.sides)):
                # these two vertices define a line segment (edge) in the subject
                # polygon. It is assumed that indices wrap around, such that if
                # j = 0, then j - 1 = N.
                print("J: ", j)
                s_vertex1 = next_s[j]
                s_vertex2 = next_s[j - 1 % len(self.sides)]
                s_side = Side(s_vertex1, s_vertex2)

                # if s_vertex2 is to the right of the line connecting c_vertex1 to c_vertex2:
                if s_vertex2.x >= min(c_vertex1.x, c_vertex2.x):
                    # if s_vertex1 is to the left of the line connecting c_vertex1 to c_vertex2:
                    if s_vertex1.x <= min(c_vertex1.x, c_vertex2.x):
                        # intersection_point = compute_intersection(s_vertex1,s_vertex2,c_vertex1,c_vertex2)
                        intersection_point = s_side.intersects(c_side)
                        if intersection_point:
                            output.append(intersection_point)
                    output.append(s_vertex2)
                # elif s_vertex1 is to the right of the line connecting c_vertex1 to c_vertex2:
                elif s_vertex1.x >= min(c_vertex1.x, c_vertex1.y):
                    # intersection_point = compute_intersection(s_vertex1,s_vertex2,c_vertex1,c_vertex2)
                    intersection_point = s_side.intersects(c_side)
                    if intersection_point:
                        output.append(intersection_point)

        clipped_area_coordinates = output
        clipped_polygon = self.from_point_list(clipped_area_coordinates)
        return clipped_polygon.area


# How to get a shapely shape from geojson
# from shapely.geometry import shape
# from shapely.geometry.polygon import Polygon
# geo: dict = {'type': 'Polygon',
#    'coordinates': [[[23.08437310100004, 53.15448536100007],
#    [23.08459767900007, 53.15448536100007],
#    [23.08594514600003, 53.153587050000056],
#    [23.08437310100004, 53.15448536100007]]]}
# polygon: Polygon = shape(geo)
