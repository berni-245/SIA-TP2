from PIL import Image
import time
from typing import Dict, Tuple, List

from src.generator import Generator, SelectionType, CrossoverType, MutationType, GenerationJumpType, ShapeType
import json

from src.individual import Individual

class ImageReconstructionGeneticAlgorithm:
    def __init__(self, og_img: Image.Image, shape_count: int):
        self._og_img = og_img
        self._shape_count = shape_count
        with open("./configs/config.json", "r") as f:
            config = json.load(f)
        self._selection = SelectionType.from_string(config["selection_algorithm"])
        self._crossover = CrossoverType.from_string(config["crossover_algorithm"])
        self._mutation = MutationType.from_string(config["mutation_algorithm"])
        self._gen_jump = GenerationJumpType.from_string(config["gen_jump_algorithm"])
        self._population_amount = config["population_amount"]
        self._generated_child_amount = config["generated_child_amount"]
        self._max_gen_count = config["max_gen_count"]
        self._min_fitness_goal = config["min_fitness_goal"]
        self._use_delta_D = config["use_delta_D"]
       
    def run(self) -> Tuple[Image.Image, float, List[Dict[str, int | Individual | float]]]:
        gen = Generator(
            self._og_img, self._shape_count, ShapeType.TRIANGLE, self._population_amount,
            self._selection, self._crossover, self._mutation, self._gen_jump, self._use_delta_D
        )
        last_fitness_check = 0
        best_fit = None
        gen_count = 0
        fitness_evolution = []

        start_time = time.time()

        while last_fitness_check <= self._min_fitness_goal and gen_count <= self._max_gen_count:
            gen_start_time = time.time()
            fittest = gen.fittest
            fitness_evolution.append({
                "gen": gen_count,
                "fittest": fittest,
                "time": time.time() - gen_start_time
            })
            if gen_count % 100 == 0:
                print(f"gen {gen_count:03}: {fittest.fitness}")
            if fittest.fitness - last_fitness_check > 0.01:
                best_fit = fittest
                last_fitness_check = best_fit.fitness
            gen.new_generation(self._generated_child_amount)
            gen_count += 1
        if best_fit == None:
            raise Exception("An error occurred and there isn't an individual with fitness greater than 0")
        return (best_fit.img, time.time() - start_time, fitness_evolution)

    def selection(self, selection: SelectionType):
        self._selection = selection
        return self

    def crossover(self, crossover: CrossoverType):
        self._crossover = crossover
        return self

    def mutation(self, mutation: MutationType):
        self._mutation = mutation
        return self

    def gen_jump(self, gen_jump: GenerationJumpType):
        self._gen_jump = gen_jump
        return self

    def population_amount(self, population_amount: int):
        self._population_amount = population_amount
        return self

    def generated_child_amount(self, generated_child_amount: int):
        self._generated_child_amount = generated_child_amount
        return self

    def max_gen_count(self, max_gen_count: int):
        self._max_gen_count = max_gen_count
        return self

    def min_fitness_goal(self, min_fitness_goal: float):
        self._min_fitness_goal = min_fitness_goal
        return self

    def use_delta_D(self):
        self._use_delta_D = True
        return self
