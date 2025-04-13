import random
from typing import Tuple, List
from abc import ABC, abstractmethod
from utils import rand_vertex, randfloat, randint, clamp
import cairo

class Shape(ABC):
    def __init__(self, color: Tuple[float,float,float,float]) -> None:
        self.color = color
        self._multiplier = 1


    @abstractmethod
    def draw(self, ctx: cairo.Context):
        pass

    @staticmethod
    @abstractmethod
    # Return type should be of the same class (Shape or its subclass)
    def random(img_size: Tuple[int,int]) -> "Shape":
        pass

    # @staticmethod
    # def random_color() -> Tuple[float,float,float,float]:
    #     return (randfloat(0, 1), randfloat(0, 1), randfloat(0, 1), randfloat(0, 1))

    def _set_multiplier(self, val: int):
        self._multiplier = val

    @abstractmethod
    def mutate(self, img_size: Tuple[int, int], multiplier_chance: float):
        pass

    @abstractmethod
    def clone(self) -> "Shape":
        """
        Create a deep copy of this shape.
        """
        pass

class Polygon(Shape):
    def __init__(self, color: Tuple[float,float,float,float], vertices: Tuple[Tuple[int,int], ...]) -> None:
        super().__init__(color)
        self.vertices = vertices

    def draw(self, ctx: cairo.Context):
        ctx.set_source_rgba(*self.color)

        ctx.move_to(*self.vertices[0])
        for point in self.vertices[1:]:
            ctx.line_to(*point)

        ctx.close_path()
        ctx.fill()

    def mutate(self, img_size: Tuple[int, int], multiplier_chance: float):
        roulette = randint(1, 100)
        if roulette <= 30: # 30% of changing color
            delta = 20/255
            self.color = (
                clamp(0, self.color[0] + randfloat(-delta, delta), 1),
                clamp(0, self.color[1] + randfloat(-delta, delta), 1),
                clamp(0, self.color[2] + randfloat(-delta, delta), 1),
                self.color[3]
            )
        elif roulette <= 40: # 10% of changing to a base color
            self.color = (*Color.get_random_fixed_color(), self.color[3])
        elif roulette <= 50: # 10% of changing transparency
            self.color = (self.color[0], self.color[1], self.color[2], Color.get_random_fixed_transparency())
        else: # 50% of changing position
            delta = ((img_size[0] + img_size[1])//(2*10)) * self._multiplier

            new_vertices = tuple(
                (clamp(0, v[0] + randint(-delta, delta), img_size[0]),
                    clamp(0, v[1] + randint(-delta, delta), img_size[1]))
                for v in self.vertices
            )
            self.vertices = new_vertices

    def __str__(self) -> str:
        return f"{{c: {self.color}, v: {self.vertices}}}"

class Triangle(Polygon):
    def __init__(self, color: Tuple[float,float,float,float], vertices: Tuple[Tuple[int,int], Tuple[int,int], Tuple[int,int]]) -> None:
        super().__init__(color, vertices)
        self.vertices = vertices

    @staticmethod
    def random(img_size: Tuple[int,int]) -> "Triangle":
        color = (*Color.get_random_fixed_color(), Color.get_full_transparency())
        # size_lim = 100
        # delta = rand_vertex(img_size)
        # x1, y1 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        # x2, y2 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        # x3, y3 = sum_vec(rand_vertex((size_lim, size_lim)), delta)

        x1, y1 = rand_vertex(img_size)
        x2, y2 = rand_vertex(img_size)
        x3, y3 = rand_vertex(img_size)
        
        return Triangle(color, ((x1, y1), (x2, y2), (x3, y3)))

    def clone(self) -> "Triangle":
        return Triangle(self.color, self.vertices)

class Square(Polygon):
    def __init__(
        self,
        color: Tuple[float,float,float,float],
        vertices: Tuple[
            Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int],
        ]
    ) -> None:
        super().__init__(color, vertices)
        self.vertices = vertices

    @staticmethod
    def random(img_size: Tuple[int,int]) -> "Square":
        color = (*Color.get_random_fixed_color(), Color.get_full_transparency())
        x1, y1 = randint(0, img_size[0]), randint(0, img_size[1])
        x3, y3 = randint(0, img_size[0]), randint(0, img_size[1])
        x2, y2 = (x3, y1)
        x4, y4 = (x1, y3)
        
        return Square(color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def clone(self) -> "Square":
        return Square(self.color, self.vertices)

# class Ellipse(Shape):
#     def __init__(self, color: Tuple[float,float,float,float], center: Tuple[int, int], radii: Tuple[int, int], angle: float = 0) -> None:
#         super().__init__(color)
#         self.center = center
#         self.radii = radii
#         self.angle = angle  # Angle in degrees for rotation
#
#     def draw(self, img_draw: ImageDraw.ImageDraw) -> None:
#         ellipse_width = self.radii[0]*2
#         ellipse_height = self.radii[1]*2
#         ellipse_img = Image.new('RGBA', (ellipse_width, ellipse_height), (0, 0, 0, 0))
#         ellipse_draw = ImageDraw.Draw(ellipse_img)
#         ellipse_draw.ellipse([0, 0, ellipse_width, ellipse_height], fill=self.color)
#         rotated_ellipse = ellipse_img.rotate(self.angle, expand=True)
#
#         # Paste the rotated ellipse onto the original image
#         corner_coords = (
#             self.center[0] - rotated_ellipse.size[0] // 2,
#             self.center[1] - rotated_ellipse.size[1] // 2
#         )
#         img_draw.bitmap(corner_coords, rotated_ellipse, fill=self.color)
#
#     @staticmethod
#     def random(cls, img_size: Tuple[int, int]) -> "Ellipse":
#         color = Shape.random_color()
#         center = (randint(0, img_size[0]), randint(0, img_size[1]))
#         radii = (randint(0, img_size[0] // 2), randint(0, img_size[1] // 2))
#         angle = randint(0, 360)
#
#         return Ellipse(color, center, radii, angle)
#
#     def mutate(self):
#         return super().mutate()
#
#     def clone(self) -> "Ellipse":
#         return Ellipse(self.color, self.center, self.radii, self.angle)

from typing import List, Tuple
from utils import randint  # o random.randint si no estás usando una función custom

class Color:
    _fixed_colors: List[Tuple[float, float, float]] = [
        (255, 0, 0),       # Red
        (0, 255, 0),       # Green
        (0, 0, 255),       # Blue
        (255, 255, 0),     # Yellow
        (255, 165, 0),     # Orange
        (128, 0, 128),     # Purple
        (0, 255, 255),     # Cyan
        (255, 192, 203),   # Pink
        (0, 0, 0),         # Black
        (255, 255, 255),   # White
        (128, 128, 128),   # Gray
        (139, 69, 19),     # Brown
        (0, 128, 0),       # Dark Green
        (0, 0, 128),       # Dark Blue
        (128, 0, 0),       # Dark Red
        (255, 20, 147),    # Fuchsia
        (173, 216, 230),   # Light Blue
        (240, 230, 140),   # Khaki
        (192, 192, 192),   # Silver
        (255, 215, 0),     # Golden
    ]

    _fixed_transparency: List[float] = [0.5, 0.75, 1]

    @classmethod
    def get_random_fixed_color(cls) -> Tuple[float, float, float]:
        color_idx = randint(0, len(cls._fixed_colors))
        R, G, B = cls._fixed_colors[color_idx]
        return (R, G, B)
    
    @classmethod
    def get_random_fixed_transparency(cls) -> float:
        transparency_idx = randint(0, len(cls._fixed_transparency))
        return cls._fixed_transparency[transparency_idx]
    
    @classmethod
    def get_full_transparency(cls) -> float:
        return 1

    