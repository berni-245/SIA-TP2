import json
import argparse
from PIL import Image
from src.generator import Generator, ShapeType, SelectionType, CrossoverType, MutationType, GenerationJumpType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run genetic image generator.")
    parser.add_argument("--image", "-i", type=str, required=True, help="Nombre del archivo de imagen.")
    parser.add_argument("--shape_count", "-s", type=int, required=True, help="Cantidad de figuras para cada individuo.")
    args = parser.parse_args()

    with open("configs/config.json", "r") as f:
        config = json.load(f)

    reference_img = Image.open(f"{args.image}").convert("RGBA")

    gen = Generator(
        reference_img, args.shape_count, ShapeType.TRIANGLE, 100,
        SelectionType.from_string(config["selection_algorithm"]),
        CrossoverType.from_string(config["crossover_algorithm"]),
        MutationType.from_string(config["mutation_algorithm"]),
        GenerationJumpType.from_string(config["gen_jump_algorithm"])
    )
    iters = 1000
    last_fitness_check = 0
    while last_fitness_check < 0.95:
        gen.new_generation(50)
        fittest = gen.fittest
        if fittest.fitness - last_fitness_check > 0.01:
            last_fitness_check = fittest.fitness

        fittest.img.save(f"./generated/fittest.png")
        print(f"Gen {gen.generation:03} - Fitness: {fittest.fitness}")
        iters -= 1
