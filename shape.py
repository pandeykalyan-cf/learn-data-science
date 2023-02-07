
from abc import ABC, abstractmethod
from dataclasses import dataclass

from point import Point



class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    @abstractmethod
    def intersect(self, other_shape: "Shape") -> float:
        pass


@dataclass
class BoundingBox(Shape):
    lower_bound: Point
    upper_bound: Point

    def area(self):
        return abs(self.upper_bound.y - self.lower_bound.y) * abs(self.upper_bound.x - self.lower_bound.x)
    
    def intersect(self, other_shape: "BoundingBox") -> float:
        xA = max(self.lower_bound.x, other_shape.lower_bound.x)
        yA = max(self.lower_bound.y, other_shape.lower_bound.y)
        xB = min(self.upper_bound.x, other_shape.upper_bound.x)
        yB = min(self.upper_bound.y, other_shape.upper_bound.y)
        return abs(xA-xB) * abs(yA-yB)


