from typing import List, Tuple
from PIL import Image
from genes import Shape
import cairo

class Individual:
    # id = 0
    def __init__(self, shapes: List[Shape], img_size: Tuple[int, int]) -> None:
        # self.id = Individual.id
        # Individual.id += 1
        self.shapes = shapes
        self.shape_count = len(shapes)

        width, height = img_size
        # Create a transparent Cairo surface
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self.surface)
        for shape in self.shapes:
            shape.draw(ctx)

        self.img = self.cairo_to_img()

        self.fitness = -1

    def set_fitness(self, fitness: float):
        self.fitness = fitness

    def cairo_to_img(self) -> Image.Image:
        buf = self.surface.get_data()
        width = self.surface.get_width()
        height = self.surface.get_height()

        # Cairo uses ARGB32 (BGRA in memory on little endian systems)
        # Pillow expects RGBA, so we need to rearrange channels
        img = Image.frombuffer("RGBA", (width, height), buf.tobytes(), "raw", "BGRA", 0, 1)
        return img

    # def __str__(self) -> str:
    #     return str(self.id)
