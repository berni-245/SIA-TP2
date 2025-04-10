from typing import Tuple
from abc import ABC, abstractmethod
from PIL import ImageDraw

class Shape(ABC):
    def __init__(self, color: Tuple[int,int,int,int]) -> None:
        self.color = color

    @abstractmethod
    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        pass


class Triangle(Shape):
    def __init__(self, color: Tuple[int,int,int,int], vertices: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> None:
        super().__init__(color)
        self.vertices = vertices

    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        img_draw.polygon(self.vertices, fill=self.color)

class Elipse(Shape):
    def __init__(self, color: Tuple[int,int,int,int], top_left: Tuple[int, int], bottom_right: Tuple[int, int]) -> None:
        super().__init__(color)
        self.top_left = top_left
        self.bottom_right = bottom_right

    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        img_draw.ellipse([*self.top_left, *self.bottom_right], fill=self.color)
