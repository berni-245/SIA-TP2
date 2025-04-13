from typing import List, Tuple
from PIL import Image
import numpy as np
import cairo
from genes import Shape
from skimage.color import rgb2lab

class Individual:
    def __init__(self, shapes: List[Shape], img_size: Tuple[int, int]) -> None:
        self.shapes = shapes
        self.shape_count = len(shapes)

        width, height = img_size
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self.surface)

        for shape in self.shapes:
            shape.draw(ctx)

        self.img = self._cairo_to_img()
        # Uncomment the lines below if you want to use the delta_D fitness
        # rgb = np.asarray(self.img.convert("RGB")) / 255.0
        # self.lab = rgb2lab(rgb)
        self.fitness = -1


    def set_fitness(self, fitness: float):
        self.fitness = fitness

    def _cairo_to_img(self) -> Image.Image:
        buf = self.surface.get_data()
        width = self.surface.get_width()
        height = self.surface.get_height()

        # Convert Cairo surface (BGRA) to Pillow image (RGBA)
        return Image.frombuffer("RGBA", (width, height), buf.tobytes(), "raw", "BGRA", 0, 1)
