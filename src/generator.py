from enum import Enum
import random
from math import ceil
from time import sleep

import colour
from utils import randint, swap_in_arr
from typing import Callable, List
import numpy as np
import random
from skimage.color import rgb2lab
from PIL import Image, ImageChops

from genes import Shape, Square, Triangle
from individual import Individual

class ShapeType(Enum):
    TRIANGLE = "Triangle"
    # ELLIPSE = "Ellipse"
    SQUARE = "Square"

class Generator:
    def __init__(self, og_img: Image.Image, shape_count: int, shape_type: ShapeType, initial_pop: int) -> None:
        self.og_img = og_img
        # Uncomment the lines below if you want to use the delta_D fitness
        # rgb = np.asarray(og_img.convert("RGB")) / 255.0
        # self.lab = rgb2lab(rgb)
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

    def _fittest_sort(self, individual: Individual) -> float:
        if individual.fitness < 0:
            return self.fitness(individual)
        else:
            return individual.fitness

    @property
    def fittest(self) -> Individual:
        return max(self.individuals, key=self._fittest_sort)

# Uncomment the lines below if you want to use the delta_D fitness, you also need to uncomment in the __init__ of generator and individual
    # def fitness_delta_D(self, individual: Individual) -> float:
    #     if individual.img.size != self.og_img.size:
    #         raise ValueError("Images must have the same dimensions.")

        # diff = colour.difference.delta_e.delta_E_CIE1976(self.lab, individual.lab)

        # mean = np.mean(diff)
        # fitness = 1 - (mean / 100)

        # fitness = max(0.0, min(1.0, float(fitness)))

        # individual.set_fitness(fitness)
        # return fitness
    
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

        mean = np.mean(np_diff)/255
        individual.set_fitness(float(1 - mean))
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

    def two_point_crossover(self, selection: List[Individual]) -> List[Individual]:
        children: List[Individual] = []
        child_remaining = len(selection) 

        while (child_remaining > 1):
            idx1 = randint(0, child_remaining)
            parent1 = selection[idx1]
            swap_in_arr(selection, idx1, child_remaining - 1)
            child_remaining -= 1

            idx2 = randint(0, child_remaining)
            parent2 = selection[idx2]
            swap_in_arr(selection, idx2, child_remaining - 1)
            child_remaining -= 1

            # parent1 = selection[randint(0, len(selection))]
            # child_remaining -= 1
            # parent2 = selection[randint(0, len(selection))]
            # child_remaining -= 1

            l1 = randint(0, parent1.shape_count)
            l2 = randint(l1, parent1.shape_count)

            child_genes1 = parent1.shapes[:l1] + parent2.shapes[l1:l2] + parent1.shapes[l2:]
            child_genes2 = parent2.shapes[:l1] + parent1.shapes[l1:l2] + parent2.shapes[l2:]
            # Make sure that the shapes in the child are copies, not references.
            # Necessary so during mutation we don't mutate the parents' genes too.
            child_genes1 = [shape.clone() for shape in child_genes1]
            child_genes2 = [shape.clone() for shape in child_genes2]
            children.append(Individual(child_genes1, self.og_img.size))
            children.append(Individual(child_genes2, self.og_img.size))

        return children

    def uniform_mutation(self, children: List[Individual], mutation_probability: float):
        for c in children:
            to_send_to_back = []
            to_send_to_front = []
            for s in c.shapes:
                rand_val = random.random()
                if rand_val <= mutation_probability / 2: # 50% of mut_prob of changing the shape's properties
                    s.mutate(self.og_img.size, 0.5)
                elif rand_val <= mutation_probability - mutation_probability/4: # 25% of mut_prob of moving the shape to the back
                    to_send_to_back.append(s)
                elif rand_val <= mutation_probability: # 25% of mut_prob of moving the shape to the front
                    to_send_to_front.append(s)
            for shape in to_send_to_back:
                c.shapes.remove(shape)
                c.shapes.append(shape)
            for shape in to_send_to_front:
                c.shapes.remove(shape)
                c.shapes.insert(0, shape)      

    def complete_mutation(self, children: List[Individual]):
        self.uniform_mutation(children, 1)

    def new_generation_young_bias(self, children: List[Individual]):
        if (len(children) <= self.population):
            new_gen = children
            if len(children) < self.population:
                chosen_parents = random.sample(self.individuals, self.population - len(children))
                # chosen_parents = random.choices(selection, k = self.population - len(children))
                new_gen.extend(chosen_parents)
        else:
            new_gen = random.sample(children, self.population)

        self.individuals = new_gen
        self.generation += 1

    def new_generation_trad(self, children: List[Individual]):
        self.individuals.extend(children)
        new_gen = random.sample(self.individuals, self.population)
        self.individuals = new_gen
        self.generation += 1

    def deterministic_tournament_selection(self, child_amount: int) -> List[Individual]:
        candidate_num = max(2, child_amount // 4) # M individuals
        children = []
        while child_amount > 0:
            chosen_candidates = random.sample(self.individuals, candidate_num)
            chosen_candidates.sort(key=self.fitness, reverse=True)
            children.append(chosen_candidates[0])
            child_amount -= 1
        return children
    
    def probabilistic_tournament_selection(self, child_amount: int) -> List[Individual]:
        threshold = random.uniform(0.5, 1)
        children = []
        while child_amount > 0:
            chosen_candidates = random.sample(self.individuals, 2)
            chosen_candidates.sort(key=self.fitness, reverse=True)
            rand_val = random.random()
            if rand_val < threshold:
                children.append(chosen_candidates[0])
            else:
                children.append(chosen_candidates[1])
            child_amount -= 1

    def ranking_selection(self, child_amount: int) -> List[Individual]:
        self.individuals.sort(key=self.fitness, reverse=True)
        return self._get_roulette_selection(
            [random.uniform(0, 1) for _ in range(child_amount)],
             self._ranking_pseudo_fitness
    )

    def _ranking_pseudo_fitness(self, ind: Individual) -> float:
        return (self.population - self.individuals.index(ind)) / self.population
        
    def universal_selection(self, child_amount: int) -> List[Individual]:
        rand_values = []
        for j in range(child_amount):
            rand_val = random.uniform(0, 1)
            rand_values.append((rand_val + j) / child_amount)
        return self._get_roulette_selection(rand_values, self.fitness)
        
    def roulette_selection(self, child_amount: int) -> List[Individual]:
        return self._get_roulette_selection([random.uniform(0, 1) for _ in range(child_amount)], self.fitness)

    def _get_roulette_selection(self, rand_values: List[float], fitness_func: Callable[[Individual], float]) -> List[Individual]:
        fitness_sum = np.sum([fitness_func(ind) for ind in self.individuals])

        accum_relative_fitness = []
        current_rel_fit = 0
        for i, ind in enumerate(self.individuals):
            current_rel_fit += ind.fitness / fitness_sum
            accum_relative_fitness.append(1 if (i+1) == len(self.individuals) else current_rel_fit)

        to_return = []
        for rand_val in rand_values:
            left_range = 0
            for ind, rel_fit in zip(self.individuals, accum_relative_fitness):
                right_range = rel_fit
                if left_range < rand_val and rand_val <= right_range:
                    to_return.append(ind)
                    break
                left_range = rel_fit
        return to_return

    # The idea would be to somehow pass as parameter which selection, crossover and mutation
    # methods we want to use.
    def new_generation(self, selection_count: int):
        selection = self.ranking_selection(selection_count)
        children = self.two_point_crossover(selection)
        self.uniform_mutation(children, 0.15)
        self.new_generation_young_bias(children)