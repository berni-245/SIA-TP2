from typing import List, Tuple
from PIL import Image, ImageDraw
from genes import Shape
import cairo

class Individual:
    def __init__(self, shapes: List[Shape], img_size: Tuple[int, int]) -> None:
        self.shapes = shapes
        self.shape_count = len(shapes)

        width, height = img_size
        # Create a transparent Cairo surface
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self.surface)

        for shape in self.shapes:
            shape.draw(ctx)

        # Convert Cairo surface to PIL Image for fitness calculations
        self.img = self.cairo_to_pil(self.surface)

    def set_fitness(self, fitness: float):
        self.fitness = fitness

    @staticmethod
    def cairo_to_pil(surface: cairo.ImageSurface) -> Image.Image:
        buf = surface.get_data()
        width = surface.get_width()
        height = surface.get_height()

        # Cairo uses ARGB32 (BGRA in memory on little endian systems)
        # Pillow expects RGBA, so we need to rearrange channels
        img = Image.frombuffer("RGBA", (width, height), buf, "raw", "BGRA", 0, 1)
        return img.copy()  # Copy to detach from Cairo's memory
