import inspect
from abc import ABC, abstractmethod
from math import sqrt

from shapely.geometry import LinearRing, LineString, Point, Polygon


class Feature(ABC):
    def __init__(self, geometry, depth=None):
        self.depth = 0 if depth is None else depth
        self.geometry = geometry

    def __repr__(self):
        return (self.name + "-" + self.shape +
                str(tuple((int(c[0]), int(c[1])) for c in self.coordinates)))

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def category(self):
        return inspect.getmodule(self).__name__.split('.')[-1].capitalize()

    @property
    @abstractmethod
    def coordinates(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def shape(self):
        raise NotImplementedError


class Position(Feature):
    shape = 'Point'

    def __init__(self, point, depth=None):
        if not (isinstance(point, tuple) and len(point) == 2):
            raise TypeError(
                f"Position should be a tuple of the form "
                f"(easting, northing) in meters"
            )
        super().__init__(Point(point), depth)

    @property
    def coordinates(self):
        return self.geometry.coords[0]

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def line_to(self, target):
        return Line(self, target)

    def is_left_of(self, line):
        positions = line.start, line.end, self
        return LinearRing((p.coordinates for p in positions)).is_ccw


class Line(Feature):
    shape = 'LineString'

    def __init__(self, start, end, depth=None):
        if not all(isinstance(p, Position) for p in (start, end)):
            raise TypeError(
                f"Line should contain exactly 2 {Position} objects"
            )
        self.start = start
        self.end = end
        self.vector = (end.x - start.x, end.y - start.y)
        self.length = sqrt(sum(i ** 2 for i in self.vector))
        geometry = LineString((start.coordinates, end.coordinates))
        super().__init__(geometry, depth)

    @property
    def coordinates(self):
        return tuple(self.geometry.coords)


class Area(Feature):
    shape = 'Polygon'

    def __init__(self, points, depth=None):
        if not all(isinstance(p, tuple) and len(p) == 2 for p in points):
            raise TypeError(
                f"Area should be a sequence of (E, N) coordinate tuples"
            )
        super().__init__(Polygon(points), depth)

    @property
    def coordinates(self):
        return tuple(self.geometry.exterior.coords)

    @property
    def area(self):
        return self.geometry.area
