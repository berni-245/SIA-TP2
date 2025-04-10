import random
from typing import Tuple
from abc import ABC, abstractmethod
from PIL import ImageDraw

class Shape(ABC):
    def __init__(self, color: Tuple[int,int,int,int]) -> None:
        self.color = color

    @abstractmethod
    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        pass

    @classmethod
    @abstractmethod
    # Return type should be of the same class (Shape or its subclass)
    def random(cls, img_size: Tuple[int, int]) -> "Shape":
        pass

class Polygon(Shape):
    def __init__(self, color: Tuple[int,int,int,int], vertices: Tuple[Tuple[int,int], ...]) -> None:
        super().__init__(color)
        self.vertices = vertices

    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        img_draw.polygon(self.vertices, fill=self.color)

class Triangle(Polygon):
    def __init__(self, color: Tuple[int,int,int,int], vertices: Tuple[Tuple[int,int], Tuple[int,int], Tuple[int,int]]) -> None:
        super().__init__(color, vertices)
        self.vertices = vertices

    @classmethod
    def random(cls, img_size: Tuple[int,int]) -> "Triangle":
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x1, y1 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        x2, y2 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        x3, y3 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        
        return Triangle(color, ((x1, y1), (x2, y2), (x3, y3)))

class Square(Polygon):
    def __init__(
            self,
            color: Tuple[int,int,int,int],
            vertices: Tuple[Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int]]
    ) -> None:
        super().__init__(color, vertices)
        self.vertices = vertices

    @classmethod
    def random(cls, img_size: Tuple[int, int]) -> "Square":
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x1, y1 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        x3, y3 = random.randint(0, img_size[0]), random.randint(0, img_size[1])
        x2, y2 = (x3, y1)
        x4, y4 = (x1, y3)
        
        return Square(color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

class Ellipse(Shape):
    def __init__(self, color: Tuple[int,int,int,int], top_left: Tuple[int, int], bottom_right: Tuple[int, int]) -> None:
        super().__init__(color)
        self.top_left = top_left
        self.bottom_right = bottom_right

    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        img_draw.ellipse([*self.top_left, *self.bottom_right], fill=self.color)

    @classmethod
    def random(cls, img_size: Tuple[int, int]) -> "Ellipse":
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x1 = random.randint(0, img_size[0] // 2)
        y1 = random.randint(0, img_size[1] // 2)
        # Ensure bottom-right is to the right and bottom of top-left
        x2 = random.randint(x1, img_size[0])
        y2 = random.randint(y1, img_size[1])
        
        return Ellipse(color, (x1, y1), (x2, y2))

