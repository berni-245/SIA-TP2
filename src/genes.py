import random
from typing import Tuple
from abc import ABC, abstractmethod
from PIL import ImageDraw
from PIL import Image

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
    def __init__(self, color: Tuple[int,int,int,int], center: Tuple[int, int], radii: Tuple[int, int], angle: float = 0) -> None:
        super().__init__(color)
        self.center = center
        self.radii = radii
        self.angle = angle  # Angle in degrees for rotation

    def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
        ellipse_width = self.radii[0]*2
        ellipse_height = self.radii[1]*2
        ellipse_img = Image.new('RGBA', (ellipse_width, ellipse_height), (0, 0, 0, 0))
        ellipse_draw = ImageDraw.Draw(ellipse_img)
        ellipse_draw.ellipse([0, 0, ellipse_width, ellipse_height], fill=self.color)
        rotated_ellipse = ellipse_img.rotate(self.angle, expand=True)

        # Paste the rotated ellipse onto the original image
        corner_coords = (
            self.center[0] - rotated_ellipse.size[0] // 2,
            self.center[1] - rotated_ellipse.size[1] // 2
        )
        img_draw.bitmap(corner_coords, rotated_ellipse, fill=self.color)

    @classmethod
    def random(cls, img_size: Tuple[int, int]) -> "Ellipse":
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        center = (random.randint(0, img_size[0]), random.randint(0, img_size[1]))
        radii = (random.randint(0, img_size[0] // 2), random.randint(0, img_size[1] // 2))
        angle = random.randint(0, 360)
        
        return Ellipse(color, center, radii, angle)
