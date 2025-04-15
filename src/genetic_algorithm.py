from enum import Enum
from PIL import Image
import time
from typing import Dict, Tuple, List

from src.generator import Generator, SelectionType, CrossoverType, MutationType, GenerationJumpType, ShapeType
import json

from src.individual import Individual

class ImageReconstructionGeneticAlgorithm:
    def __init__(self, og_img: Image.Image, shape_count: int):
        self.og_img = og_img
        self.shape_count = shape_count
        with open("./configs/config.json", "r") as f:
            config = json.load(f)
        self.selection = SelectionType.from_string(config["selection_algorithm"])
        self.crossover = CrossoverType.from_string(config["crossover_algorithm"])
        self.mutation = MutationType.from_string(config["mutation_algorithm"])
        self.gen_jump = GenerationJumpType.from_string(config["gen_jump_algorithm"])
        self.population_amount = config["population_amount"]
        self.generated_child_amount = config["generated_child_amount"]
        self.max_gen_count = config["max_gen_count"]
        self.min_fitness_goal = config["min_fitness_goal"]
       
    def run(self) -> Tuple[Image.Image, float, List[Dict[str, int | Individual | float]]]:
        gen = Generator(
            self.og_img, self.shape_count, ShapeType.TRIANGLE, self.population_amount,
            self.selection, self.crossover, self.mutation, self.gen_jump
        )
        last_fitness_check = 0
        best_fit = None
        gen_count = 0
        fitness_evolution = []

        start_time = time.time()

        while last_fitness_check <= self.min_fitness_goal and gen_count <= self.max_gen_count:
            gen_start_time = time.time()
            fittest = gen.fittest
            fitness_evolution.append({
                "gen": gen_count,
                "fittest": fittest,
                "time": time.time() - gen_start_time
            })
            if fittest.fitness - last_fitness_check > 0.01:
                best_fit = fittest
                last_fitness_check = best_fit.fitness
            gen.new_generation(self.generated_child_amount)
            gen_count += 1
        if best_fit == None:
            raise Exception("An error occurred and there isn't an individual with fitness greater than 0")
        return (best_fit.img, time.time() - start_time, fitness_evolution)

    def set_selection(self, selection: SelectionType):
        self.selection = selection
        return self

    def set_crossover(self, crossover: CrossoverType):
        self.crossover = crossover
        return self

    def set_mutation(self, mutation: MutationType):
        self.mutation = mutation
        return self

    def set_gen_jump(self, gen_jump: GenerationJumpType):
        self.gen_jump = gen_jump
        return self

    def set_population_amount(self, population_amount: int):
        self.population_amount = population_amount
        return self

    def set_generated_child_amount(self, generated_child_amount: int):
        self.generated_child_amount = generated_child_amount
        return self

    def set_max_gen_count(self, max_gen_count: int):
        self.max_gen_count = max_gen_count
        return self

    def set_min_fitness_goal(self, min_fitness_goal: float):
        self.min_fitness_goal = min_fitness_goal
        return self
