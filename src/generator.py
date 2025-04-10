from enum import Enum
from typing import List
import numpy as np

from PIL import Image, ImageChops

from genes import Ellipse, Shape, Square, Triangle
from individual import Individual

class ShapeType(Enum):
    TRIANGLE = "Triangle"
    ELLIPSE = "Ellipse"
    SQUARE = "Square"

class Generator:
    def __init__(self, og_img: Image.Image, shape_count: int, shape_type: ShapeType, initial_pop: int) -> None:
        self.og_img = og_img
        self.shape_count = shape_count
        if shape_type == ShapeType.TRIANGLE:
            self.shape = Triangle
        if shape_type == ShapeType.ELLIPSE:
            self.shape = Ellipse
        if shape_type == ShapeType.SQUARE:
            self.shape = Square

        self.individuals: List[Individual] = []

        for _ in range(0, initial_pop):
            shapes: List[Shape] = []
            for _ in range(0, shape_count):
                shapes.append(self.shape.random(og_img.size))
            individual = Individual(shapes, og_img.size)
            self.individuals.append(individual)

    # Value closer to 0 is more similar.
    def fitness(self, individual: Individual) -> np.double:
        if individual.img.size != self.og_img.size:
            raise ValueError("Images must have the same dimensions.")

        diff = ImageChops.difference(individual.img, self.og_img)
        np_diff = np.array(diff)

        return np.mean(np_diff)
