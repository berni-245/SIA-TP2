from typing import Tuple
from abc import ABC, abstractmethod
from utils import rand_vertex, randfloat, randint, clamp
import cairo

class Shape(ABC):
    def __init__(self, color: Tuple[float,float,float,float], img_size: Tuple[int, int]) -> None:
        self.color = color
        self.img_size = img_size

    @abstractmethod
    def draw(self, ctx: cairo.Context):
        pass

    @staticmethod
    @abstractmethod
    # Return type should be of the same class (Shape or its subclass)
    def random(img_size: Tuple[int,int]) -> "Shape":
        pass

    @staticmethod
    def random_color() -> Tuple[float,float,float,float]:
        return (randfloat(0, 1), randfloat(0, 1), randfloat(0, 1), randfloat(0, 1))

    @abstractmethod
    def mutate(self):
        # Max change in color channel
        delta = 20/255

        new_color = (
            clamp(0, self.color[0] + randfloat(-delta, delta), 1),
            clamp(0, self.color[1] + randfloat(-delta, delta), 1),
            clamp(0, self.color[2] + randfloat(-delta, delta), 1),
            clamp(0, self.color[3] + randfloat(-delta, delta), 1),
        )
        self.color = new_color

    @abstractmethod
    def clone(self) -> "Shape":
        """
        Create a deep copy of this shape.
        """
        pass

class Polygon(Shape):
    def __init__(self, color: Tuple[float,float,float,float], img_size: Tuple[int, int], vertices: Tuple[Tuple[int,int], ...]) -> None:
        super().__init__(color, img_size)
        self.vertices = vertices

    def draw(self, ctx: cairo.Context):
        ctx.set_source_rgba(*self.color)

        ctx.move_to(*self.vertices[0])
        for point in self.vertices[1:]:
            ctx.line_to(*point)

        ctx.close_path()
        ctx.fill()

    def mutate(self):
        super().mutate()
        # Max change in vertex position
        delta = 50

        new_vertices = tuple(
            (clamp(0, v[0] + randint(-delta, delta), self.img_size[0]),
             clamp(0, v[1] + randint(-delta, delta), self.img_size[1]))
            for v in self.vertices
        )
        self.vertices = new_vertices

    def __str__(self) -> str:
        return f"{{c: {self.color}, v: {self.vertices}}}"

class Triangle(Polygon):
    def __init__(self, color: Tuple[float,float,float,float], img_size: Tuple[int, int], vertices: Tuple[Tuple[int,int], Tuple[int,int], Tuple[int,int]]) -> None:
        super().__init__(color, img_size, vertices)
        self.vertices = vertices

    @staticmethod
    def random(img_size: Tuple[int,int]) -> "Triangle":
        color = Shape.random_color()
        # size_lim = 100
        # delta = rand_vertex(img_size)
        # x1, y1 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        # x2, y2 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        # x3, y3 = sum_vec(rand_vertex((size_lim, size_lim)), delta)

        x1, y1 = rand_vertex(img_size)
        x2, y2 = rand_vertex(img_size)
        x3, y3 = rand_vertex(img_size)
        
        return Triangle(color, img_size, ((x1, y1), (x2, y2), (x3, y3)))

    def clone(self) -> "Triangle":
        return Triangle(self.color, self.img_size, self.vertices)

class Square(Polygon):
    def __init__(
        self,
        color: Tuple[float,float,float,float],
        img_size: Tuple[int, int],
        vertices: Tuple[
            Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int],
            Tuple[int,int],
        ]
    ) -> None:
        super().__init__(color, img_size, vertices)
        self.vertices = vertices

    @staticmethod
    def random(img_size: Tuple[int,int]) -> "Square":
        color = Shape.random_color()
        x1, y1 = randint(0, img_size[0]), randint(0, img_size[1])
        x3, y3 = randint(0, img_size[0]), randint(0, img_size[1])
        x2, y2 = (x3, y1)
        x4, y4 = (x1, y3)
        
        return Square(color, img_size, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def clone(self) -> "Square":
        return Square(self.color, self.img_size, self.vertices)

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
