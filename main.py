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

    genetic_algorithm = ImageReconstructionGeneticAlgorithm(reference_img, args.shape_count)
    img, elapsed_time, fitness_evolution = genetic_algorithm.run()
    img.save(f"./generated/{image_path.name}")
    print(f"Elapsed time: {elapsed_time}")
    print(f"Final gen: {len(fitness_evolution) - 1}")
