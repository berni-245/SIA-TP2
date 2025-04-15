import json
import argparse
from pathlib import Path
from PIL import Image
from src.genetic_algorithm import ImageReconstructionGeneticAlgorithm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run genetic image generator.")
    parser.add_argument("--image", "-i", type=str, required=True, help="Nombre del archivo de imagen.")
    parser.add_argument("--shape_count", "-s", type=int, required=True, help="Cantidad de figuras para cada individuo.")
    args = parser.parse_args()

    with open("configs/config.json", "r") as f:
        config = json.load(f)

    image_path = Path(args.image)
    reference_img = Image.open(f"{image_path}").convert("RGBA")
    # (w,h) = reference_img.size
    # reference_img.resize((w//2,h//2)).save(f"./assets/small-{image_path.name}")

    genetic_algorithm = ImageReconstructionGeneticAlgorithm(reference_img, args.shape_count)
    fitness_evolution, elapsed_time = genetic_algorithm.run()

    fittest_individual = max(fitness_evolution, key=lambda x: x['fittest'].fitness)
    fittest = fittest_individual['fittest']
    best_gen = fittest_individual['gen']
    fittest.img.save(f"./generated/{image_path.name}")
    print(f"Elapsed time: {elapsed_time}")
    print(f"Final gen: {len(fitness_evolution) - 1}")
    print(f"Fittest gen: {best_gen}")
    print(f"Max fitness: {fittest.fitness}")
