import math
import random
import numpy as np
import random
import colour
from enum import Enum
from math import ceil
from typing import Callable, Dict, List
from skimage.color import rgb2lab
from PIL import Image, ImageChops
from src.genes import Shape, Square, Triangle
from src.individual import Individual
from src.utils import randint, swap_in_arr

class ShapeType(Enum):
    TRIANGLE = "Triangle"
    # ELLIPSE = "Ellipse"
    SQUARE = "Square"

class SelectionType(Enum): 
    ELITE = 1
    ROULETTE = 2
    UNIVERSAL = 3
    BOLTZMANN = 4
    DETERMINISTIC_TOURNAMENT = 5
    PROBABILISTIC_TOURNAMENT = 6
    RANKING = 7

    @classmethod
    def from_string(cls, name: str):
        return cls[name.upper()]

class CrossoverType(Enum):
    TWO_POINT = 1
    UNIFORM = 2

    @classmethod
    def from_string(cls, name: str):
        return cls[name.upper()]

class MutationType(Enum):
    UNIFORM = 1
    COMPLETE = 2

    @classmethod
    def from_string(cls, name: str):
        return cls[name.upper()]

class GenerationJumpType(Enum):
    TRADITIONAL = 1
    YOUNG_BIAS = 2

    @classmethod
    def from_string(cls, name: str):
        return cls[name.upper()]

class Generator:
    def __init__(
        self,
        og_img: Image.Image,
        shape_count: int,
        shape_type: ShapeType,
        initial_pop: int,
        selection_type: SelectionType,
        crossover_type: CrossoverType,
        mutation_type: MutationType,
        generation_jump_type: GenerationJumpType,
        use_delta_D: bool = False
    ) -> None:
        self.og_img = og_img

        self.use_delta_D = use_delta_D

        # Uncomment the lines below if you want to use the delta_D fitness
        if use_delta_D:
            rgb = np.asarray(og_img.convert("RGB")) / 255.0
            self.lab = rgb2lab(rgb)
            self.fitness_func = self.fitness_delta_D
        else:
            self.fitness_func = self.fitness_euclidean

        self.shape_count = shape_count
        if shape_type == ShapeType.TRIANGLE:
            self.shape = Triangle
        # if shape_type == ShapeType.ELLIPSE:
        #     self.shape = Ellipse
        if shape_type == ShapeType.SQUARE:
            self.shape = Square

        self.generation = 0
        self.population = initial_pop

        self._create_candidates_dicts()
        self.selection = self.selections_candidates[selection_type]
        self.crossover = self.crossover_candidates[crossover_type]
        self.mutation = self.mutation_cadidates[mutation_type]
        self.init_mutation = 0.9
        self.mutation_prob = self.init_mutation
        self.generation_jump = self.generation_jump_candidates[generation_jump_type]

        self.individuals: List[Individual] = []

        for _ in range(initial_pop):
            shapes: List[Shape] = []
            for _ in range(shape_count):
                shapes.append(self.shape.random(og_img.size))
            individual = Individual(shapes, og_img.size, self.use_delta_D)
            self.individuals.append(individual)

    def _fittest_sort(self, individual: Individual) -> float:
        if individual.fitness < 0:
            return self.fitness_func(individual)
        else:
            return individual.fitness

    @property
    def fittest(self) -> Individual:
        return max(self.individuals, key=self._fittest_sort)

# Uncomment the lines below if you want to use the delta_E fitness, you also need to uncomment in the __init__ of generator and individual
    def fitness_delta_D(self, individual: Individual) -> float:
        if individual.img.size != self.og_img.size:
            raise ValueError("Images must have the same dimensions.")

        diff = colour.difference.delta_e.delta_E_CIE1976(self.lab, individual.lab)

        mean = np.mean(diff)
        fitness = 1 - (mean / 100)

        fitness = max(0.0, min(1.0, float(fitness)))

        individual.set_fitness(fitness)
        return fitness
    
    def fitness_euclidean(self, individual: Individual) -> float:
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
        individual.set_fitness(float(1 - mean)**2)
        return individual.fitness

    def _elite_selection_individual_amount(self, selection_count: int, individual_idx: int) -> int:
        return ceil((selection_count - individual_idx)/self.population)

    def elite_selection(self, selection_count: int) -> List[Individual]:
        self.individuals.sort(key=self.fitness_func, reverse=True)
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
            children.append(Individual(child_genes1, self.og_img.size, self.use_delta_D))
            children.append(Individual(child_genes2, self.og_img.size, self.use_delta_D))

        return children
    
    def uniform_crossover(self, selection: List[Individual], prob_of_gen_swap: float = 0.5) -> List[Individual]:
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

            child_gens1 = []
            child_gens2 = []
            for i in range(min(len(parent1.shapes), len(parent2.shapes))):
                if random.random() < prob_of_gen_swap:
                    child_gens1.append(parent2.shapes[i].clone())
                    child_gens2.append(parent1.shapes[i].clone())
                else:
                    child_gens1.append(parent1.shapes[i].clone())
                    child_gens2.append(parent2.shapes[i].clone())

            children.append(Individual(child_gens1, self.og_img.size, self.use_delta_D))
            children.append(Individual(child_gens2, self.og_img.size, self.use_delta_D))

        return children

    def uniform_mutation(self, children: List[Individual]):
        for c in children:
            to_send_to_back = []
            to_send_to_front = []
            for s in c.shapes:
                rand_val = random.random()
                if rand_val <= self.mutation_prob / 2: # 50% of mut_prob of changing the shape's properties
                    s.mutate(self.og_img.size)
                elif rand_val <= self.mutation_prob - self.mutation_prob/4: # 25% of mut_prob of moving the shape to the back
                    to_send_to_back.append(s)
                elif rand_val <= self.mutation_prob: # 25% of mut_prob of moving the shape to the front
                    to_send_to_front.append(s)
            for shape in to_send_to_back:
                c.shapes.remove(shape)
                c.shapes.append(shape)
            for shape in to_send_to_front:
                c.shapes.remove(shape)
                c.shapes.insert(0, shape)      

    def complete_mutation(self, children: List[Individual]):
        if random.random() <= self.mutation_prob:
            self.uniform_mutation(children)

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
            chosen_candidates.sort(key=self.fitness_func, reverse=True)
            children.append(chosen_candidates[0])
            child_amount -= 1
        return children
    
    def probabilistic_tournament_selection(self, child_amount: int) -> List[Individual]:
        threshold = random.uniform(0.5, 1)
        children = []
        while child_amount > 0:
            chosen_candidates = random.sample(self.individuals, 2)
            chosen_candidates.sort(key=self.fitness_func, reverse=True)
            rand_val = random.random()
            if rand_val < threshold:
                children.append(chosen_candidates[0])
            else:
                children.append(chosen_candidates[1])
            child_amount -= 1
        return children
    
    def boltzmann_selection(self, child_amount: int) -> List[Individual]:
        # k: the lower number this is, the "slower" the temperature will decrease,
        # the number was calculated with a max_gen of 2000 in mind using k = -math.log(tc/t0) / max_gen
        temp = self._temperature(1.0, 0.1, 0.0023)
        self._boltzmann_mean = np.mean([
            math.exp(self.fitness_func(indi) / temp) for indi in self.individuals
        ])
        return self._get_roulette_selection(
            [random.uniform(0, 1) for _ in range(child_amount)],
            lambda ind: self._boltzmann_pseudo_fitness(ind, temp)
        )

    def _temperature(self, temp_i: float, temp_f: float, k: float):
        return temp_f + (temp_i - temp_f)*math.exp(-k*self.generation)

    def _boltzmann_pseudo_fitness(self, ind: Individual, temp: float) -> float:
        return float(math.exp(self.fitness_func(ind) / temp) / self._boltzmann_mean)

    def ranking_selection(self, child_amount: int) -> List[Individual]:
        self.individuals.sort(key=self.fitness_func, reverse=True)
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
        return self._get_roulette_selection(rand_values, self.fitness_func)
        
    def roulette_selection(self, child_amount: int) -> List[Individual]:
        return self._get_roulette_selection([random.uniform(0, 1) for _ in range(child_amount)], self.fitness_func)

    def _get_roulette_selection(self, rand_values: List[float], fitness_func: Callable[[Individual], float]) -> List[Individual]:
        fitness_sum = np.sum([fitness_func(ind) for ind in self.individuals])

        accum_relative_fitness = []
        current_rel_fit = 0
        for i, ind in enumerate(self.individuals):
            current_rel_fit += fitness_func(ind) / fitness_sum
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
        selection = self.selection(selection_count)
        children = self.crossover(selection)
        self.mutation(children)
        self.generation_jump(children)
        self.mutation_prob = self._temperature(self.init_mutation, 0.08, 0.0014)

    def _create_candidates_dicts(self):
        self.selections_candidates: Dict[SelectionType, Callable[[int], List[Individual]]] = {
            SelectionType.ELITE: self.elite_selection,
            SelectionType.ROULETTE: self.roulette_selection,
            SelectionType.UNIVERSAL: self.universal_selection,
            SelectionType.RANKING: self.ranking_selection,
            SelectionType.BOLTZMANN: self.boltzmann_selection,
            SelectionType.DETERMINISTIC_TOURNAMENT: self.deterministic_tournament_selection,
            SelectionType.PROBABILISTIC_TOURNAMENT: self.probabilistic_tournament_selection,
        }

        self.crossover_candidates: Dict[CrossoverType, Callable[[List[Individual]], List[Individual]]] = {
            CrossoverType.TWO_POINT: self.two_point_crossover,
            CrossoverType.UNIFORM: self.uniform_crossover
        }

        self.mutation_cadidates: Dict[MutationType, Callable[[List[Individual]], None]] = {
            MutationType.UNIFORM: self.uniform_mutation,
            MutationType.COMPLETE: self.complete_mutation
        }

        self.generation_jump_candidates: Dict[GenerationJumpType, Callable[[List[Individual]], None]] = {
            GenerationJumpType.TRADITIONAL: self.new_generation_trad,
            GenerationJumpType.YOUNG_BIAS: self.new_generation_young_bias
        }
