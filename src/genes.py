from typing import Tuple
from abc import ABC, abstractmethod
from PIL import ImageDraw
from PIL import Image
from utils import rand_vertex, randint, clamp, sum_vec
import cairo

class Shape(ABC):
    def __init__(self, color: Tuple[int,int,int,int]) -> None:
        self.color = color

    @abstractmethod
    def draw(self, ctx: cairo.Context):
        pass

    @classmethod
    @abstractmethod
    # Return type should be of the same class (Shape or its subclass)
    def random(cls, img_size: Tuple[int, int]) -> "Shape":
        pass

    @abstractmethod
    def mutate(self):
        # Max change in color channel
        delta = 20

        new_color:  Tuple[int,int,int,int] = (
            clamp(0, self.color[0] + randint(-delta, delta), 255),
            clamp(0, self.color[1] + randint(-delta, delta), 255),
            clamp(0, self.color[2] + randint(-delta, delta), 255),
            clamp(0, self.color[3] + randint(-delta, delta), 255),
        )
        self.color = new_color

    @abstractmethod
    def clone(self) -> "Shape":
        """
        Create a deep copy of this shape.
        """
        pass

class Polygon(Shape):
    def __init__(self, color: Tuple[int,int,int,int], vertices: Tuple[Tuple[int,int], ...]) -> None:
        super().__init__(color)
        self.vertices = vertices

    def draw(self, ctx: cairo.Context):
        # Normalize RGBA to 0–1
        r, g, b, a = [c / 255.0 for c in self.color]

        # Set color with alpha
        ctx.set_source_rgba(r, g, b, a)

        # Move to first point
        ctx.move_to(*self.vertices[0])

        # Draw lines to other points
        for point in self.vertices[1:]:
            ctx.line_to(*point)

        # Close the triangle and fill
        ctx.close_path()
        ctx.fill()

    def mutate(self):
        super().mutate()
        # Max change in vertex position
        delta = 200

        new_vertices = tuple(
            (v[0] + randint(-delta, delta), v[1] + randint(-delta, delta))
            for v in self.vertices
        )
        self.vertices = new_vertices

    def __str__(self) -> str:
        return f"{{c: {self.color}, v: {self.vertices}}}"

class Triangle(Polygon):
    def __init__(self, color: Tuple[int,int,int,int], vertices: Tuple[Tuple[int,int], Tuple[int,int], Tuple[int,int]]) -> None:
        super().__init__(color, vertices)
        self.vertices = vertices

    @classmethod
    def random(cls, img_size: Tuple[int,int]) -> "Triangle":
        color = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
        size_lim = 100
        delta = rand_vertex(img_size)
        x1, y1 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        x2, y2 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        x3, y3 = sum_vec(rand_vertex((size_lim, size_lim)), delta)
        
        return Triangle(color, ((x1, y1), (x2, y2), (x3, y3)))

    def clone(self) -> "Triangle":
        return Triangle(self.color, self.vertices)

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
        color = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
        x1, y1 = randint(0, img_size[0]), randint(0, img_size[1])
        x3, y3 = randint(0, img_size[0]), randint(0, img_size[1])
        x2, y2 = (x3, y1)
        x4, y4 = (x1, y3)
        
        return Square(color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def clone(self) -> "Square":
        return Square(self.color, self.vertices)

# class Ellipse(Shape):
#     def __init__(self, color: Tuple[int,int,int,int], center: Tuple[int, int], radii: Tuple[int, int], angle: float = 0) -> None:
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
#     @classmethod
#     def random(cls, img_size: Tuple[int, int]) -> "Ellipse":
#         color = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
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
