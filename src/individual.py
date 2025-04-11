from typing import List, Tuple

from PIL import Image, ImageDraw
from genes import Shape

class Individual:
    def __init__(self, shapes: List[Shape], img_size: Tuple[int, int]) -> None:
        self.shapes = shapes
        self.shape_count = len(shapes)
        self.img = Image.new("RGBA", img_size, (255, 255, 255, 0))
        img_draw = ImageDraw.Draw(self.img, "RGBA")
        for shape in self.shapes:
            # Create a new transparent image for each shape
            shape_layer = Image.new("RGBA", img_size, (255, 255, 255, 0))
            img_draw = ImageDraw.Draw(shape_layer)
            shape.draw(img_draw)
            
            # Use alpha_composite to layer the shape on top of the existing image
            self.img = Image.alpha_composite(self.img, shape_layer)

    def set_fitness(self, fitness: float):
        self.fitness = fitness
