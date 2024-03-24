from json import loads as json_loads

from django.test import TestCase

from yourballot.locality.geo.shape import Point, Polygon, Side


class TestPolygon(TestCase):
    """
    Tests for the creation of polygons from geojson and the calculation of their area and
    the area of intersection of two polygons
    """

    def test_create_polygon_from_geojson(self) -> None:
        sample_geojson: str = """
        {
          "type": "Polygon",
          "coordinates": [
            [
              [30.0, 10.0],
              [40.0, 40.0],
              [20.0, 40.0],
              [10.0, 20.0],
              [30.0, 10.0]
            ]
          ]
        }
        """
        parsed_data = json_loads(sample_geojson)
        polygon = Polygon.from_geojson(parsed_data)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.sides), 5)

        coordinates = [[30.0, 10.0], [40.0, 40.0], [20.0, 40.0], [10.0, 20.0], [30.0, 10.0]]
        expected_points: list[Point] = []
        for coordinate in coordinates:
            expected_points.append(Point(*coordinate))

        expected_sides: list[Side] = []
        for i in range(len(expected_points) - 1):
            expected_sides.append(Side(expected_points[i], expected_points[i + 1]))

        expected_sides.append(Side(expected_points[-1], expected_points[0]))
        self.assertSequenceEqual(expected_sides, polygon.sides)

    def test_create_triangle_from_geojson(self) -> None:
        points = [[0, 0], [2, 2], [4, 0]]
        parsed_data = {
            "type": "Polygon",
            "coordinates": [
                points,
            ],
        }
        polygon = Polygon.from_geojson(parsed_data)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.sides), 3)

        expected_points = [Point(*point) for point in points]
        expected_sides: list[Side] = []
        for i in range(len(expected_points) - 1):
            expected_sides.append(Side(expected_points[i], expected_points[i + 1]))
        expected_sides.append(Side(expected_points[-1], expected_points[0]))
        self.assertSequenceEqual(expected_sides, polygon.sides)

    def test_point_inside_polygon(self) -> None:
        points = [[0, 0], [2, 2], [4, 0]]
        parsed_data = {
            "type": "Polygon",
            "coordinates": [
                points,
            ],
        }
        polygon = Polygon.from_geojson(parsed_data)

        outside_point = Point(-1, -1)
        self.assertFalse(polygon.point_is_inside(outside_point))

        inside_point = Point(1, 1)
        self.assertTrue(polygon.point_is_inside(inside_point))

        point_on_edge = Point(0, 0)
        self.assertTrue(polygon.point_is_inside(point_on_edge))

        inside_point = Point(2.01, 1.7)
        self.assertTrue(polygon.point_is_inside(inside_point))

    def test_point_intersection_of_sides(self) -> None:
        side_one = Side(Point(-1, 0), Point(1, 0))
        side_two = Side(Point(0, -1), Point(0, 1))

        self.assertEqual(side_one.intersects(side_two), Point(0, 0))

        side_one = Side(Point(5, 5), Point(5, 15))
        side_two = Side(Point(0, 0), Point(7, 0))
        self.assertIsNone(side_one.intersects(side_two))
