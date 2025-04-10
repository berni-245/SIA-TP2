from enum import Enum
from typing import List

from PIL import Image

from genes import Elipse, Shape, Triangle
from individual import Individual

class ShapeType(Enum):
    TRIANGLE = "Triangle"
    ELLIPSE = "Ellipse"

class Generator:
    def __init__(self, og_img: Image.Image, shape_count: int, shape_type: ShapeType, initial_pop: int) -> None:
        self.og_img = og_img
        self.shape_count = shape_count
        if shape_type == ShapeType.TRIANGLE:
            self.shape = Triangle
        if shape_type == ShapeType.ELLIPSE:
            self.shape = Elipse

        self.individuals: List[Individual] = []

        for _ in range(1, initial_pop):
            shapes: List[Shape] = []
            for _ in range(1, shape_count):
                shapes.append(self.shape.random(og_img.size))
            individual = Individual(shapes, og_img.size)
            self.individuals.append(individual)

