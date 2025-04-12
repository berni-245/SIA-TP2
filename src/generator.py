from enum import Enum
import random
from math import ceil
from utils import randint
from typing import List
import numpy as np
import random

from PIL import Image, ImageChops

from genes import Shape, Square, Triangle
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
        # if shape_type == ShapeType.ELLIPSE:
        #     self.shape = Ellipse
        if shape_type == ShapeType.SQUARE:
            self.shape = Square

        self.generation = 0
        self.population = initial_pop

        self.individuals: List[Individual] = []

        for _ in range(initial_pop):
            shapes: List[Shape] = []
            for _ in range(shape_count):
                shapes.append(self.shape.random(og_img.size))
            individual = Individual(shapes, og_img.size)
            self.individuals.append(individual)

    @property
    def fittest(self) -> Individual:
        return max(self.individuals, key=self.fitness)

    def fitness(self, individual: Individual) -> float:
        """
        Calculate the fitness of an individual by comparing its image to the original image.

        @param `individual: Individual`: The individual whose fitness is to be evaluated.
        @returns `np.double`: A value in the range (0, 1], with 1 representing a perfect match.
        """
        if individual.img.size != self.og_img.size:
            raise ValueError("Images must have the same dimensions.")

        diff = ImageChops.difference(individual.img, self.og_img)
        np_diff = np.array(diff)

        individual.set_fitness(float(1 / (np.mean(np_diff) + 1)))
        return individual.fitness

    def _elite_selection_individual_amount(self, selection_count: int, individual_idx: int) -> int:
        return ceil((selection_count - individual_idx)/self.population)

    def elite_selection(self, selection_count: int) -> List[Individual]:
        self.individuals.sort(key=self.fitness, reverse=True)
        selected = []
        for i in range(0, self.population):
            count = self._elite_selection_individual_amount(selection_count, i)
            # WARNING: individuals in `selected` will be references to the originals.
            selected.extend([self.individuals[i]] * count)

        return selected

    def two_point_crossover(self, selection: List[Individual], child_count: int) -> List[Individual]:
        children: List[Individual] = []
        for _ in range(0, child_count):
            # Note that both parents could be the same individual, not sure if this is correct...
            parent1 = selection[randint(0, len(selection))]
            parent2 = selection[randint(0, len(selection))]
            # print(f"p1l: {len(parent1.shapes)}, p2l: {len(parent2.shapes)}")
            l1 = randint(0, parent1.shape_count)
            l2 = randint(l1, parent1.shape_count)
            # print(f"l1: {l1}, l2: {l2}")

            child_genes = parent1.shapes[:l1] + parent2.shapes[l1:l2] + parent1.shapes[l2:]
            # Make sure that the shapes in the child are copies, not references.
            # Necessary so during mutation we don't mutate the parents' genes too.
            child_genes = [shape.clone() for shape in child_genes]
            # print(f"cgl: {len(child_genes)}")
            children.append(Individual(child_genes, self.og_img.size))

        return children

    def uniform_mutation(self, children: List[Individual], mutation_probability: float):
        for c in children:
            for s in c.shapes:
                if random.random() < mutation_probability:
                    s.mutate()

    def new_generation_young_bias(self, selection: List[Individual], children: List[Individual]):
        if (len(children) <= self.population):
            new_gen = children
            self.uniform_mutation(new_gen, 0.8)
            if len(children) < self.population:
                # chosen_parents = random.sample(self.individuals, self.population - len(children))
                chosen_parents = random.choices(selection, k = self.population - len(children))
                new_gen.extend(chosen_parents)
        else:
            new_gen = random.sample(children, self.population)
            self.uniform_mutation(new_gen, 0.8)

        self.individuals = new_gen
        self.generation += 1


    # The idea would be to somehow pass as parameter which selection, crossover and mutation
    # methods we want to use.
    def new_generation(self, selection_count: int, child_count: int):
        selection = self.elite_selection(selection_count)
        chilren = self.two_point_crossover(selection, child_count)
        self.new_generation_young_bias(selection, chilren)
    
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
        fitness_sum = np.sum([self.fitness(ind) for ind in self.individuals])

        accum_relative_fitness = []
        current_rel_fit = 0
        for i, ind in enumerate(individuals):
            current_rel_fit += ind.fitness / fitness_sum
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
