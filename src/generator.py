from enum import Enum
import random
from typing import List
import numpy as np

from PIL import Image, ImageChops
from traitlets import Float

from genes import Ellipse, Shape, Square, Triangle
from individual import Individual

import sys

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

        for _ in range(initial_pop):
            shapes: List[Shape] = []
            for _ in range(shape_count):
                shapes.append(self.shape.random(og_img.size))
            individual = Individual(shapes, og_img.size)
            self.individuals.append(individual)

    # Value closer to 0 is more similar.
    def fitness_inverse(self, individual: Individual) -> np.double:
        if individual.img.size != self.og_img.size:
            raise ValueError("Images must have the same dimensions.")

        diff = ImageChops.difference(individual.img, self.og_img)
        np_diff = np.array(diff)

        return np.mean(np_diff) + 1
    
    def fitness(self, individual: Individual) -> np.double:
        fit_inv = self.fitness_inverse(individual)
        return 1 / fit_inv

    def relative_fitness(self, individual: Individual) -> np.double:
        fitness_arr = [self.fitness(ind) for ind in self.individuals]

        return self.fitness(individual) / np.sum(fitness_arr)
    
    def trad_generational_jump(self):
        individuals_size = len(self.individuals)

        for _ in range(individuals_size):
            shapes: List[Shape] = []
            for _ in range(self.shape_count):
                shapes.append(self.shape.random(self.og_img.size))
            individual = Individual(shapes, self.og_img.size)
            self.individuals.append(individual)

        self.individuals = self.universal_selection(self.individuals, individuals_size)
        

    
    def universal_selection(self, individuals: List[Individual], child_amount: int) -> List[Individual]:
        rand_values = []
        for j in range(child_amount):
            rand_val = random.uniform(0, 1)
            rand_values.append((rand_val + j) / child_amount)
        return self._get_roulette_selection(individuals, rand_values)
        
    def roulette_selection(self, individuals: List[Individual], child_amout: int) -> List[Individual]:
        return self._get_roulette_selection(individuals, [random.uniform(0, 1) for _ in range(child_amout)])


    def _get_roulette_selection(self, individuals: List[Individual], rand_values: List[float]) -> List[Individual]:
        accum_relative_fitness = []
        current_rel_fit = 0
        for i, ind in enumerate(individuals):
            current_rel_fit += self.relative_fitness(ind)
            accum_relative_fitness.append(1 if (i+1) == len(individuals) else current_rel_fit)

        to_return = []
        for rand_val in rand_values:
            left_range = 0
            for ind, rel_fit in zip(individuals, accum_relative_fitness):
                right_range = rel_fit
                if left_range < rand_val and rand_val <= right_range:
                    to_return.append(ind)
                    break
                left_range = rel_fit
        return to_return
