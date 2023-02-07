
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from shape import BoundingBox, Shape

# class Intersection(ABC):

#     @abstractmethod
#     def intersection(self) -> float:
#         pass

# def IntersectionFactory(ground_truth: Shape, annotated: Shape) -> Intersection:
#     if type(ground_truth) != type(annotated):
#             raise ValueError("Both ground_truth and annotated should be of same type.")
        
#     if isinstance(ground_truth, BoundingBox) and isinstance(annotated, BoundingBox):
#         return BoundingBoxIntersection(ground_truth, annotated)

#     return None

# @dataclass
# class BoundingBoxIntersection:

#     def intersection(self, ) -> float:
#         xA = max(self.ground_truth.lower_bound.x, self.annotated.lower_bound.x)
#         yA = max(self.ground_truth.lower_bound.y, self.annotated.lower_bound.y)
#         xB = min(self.ground_truth.upper_bound.x, self.annotated.upper_bound.x)
#         yB = min(self.ground_truth.upper_bound.x, self.annotated.upper_bound.x)

#         return abs(xA-xB) * abs(yA-yB)