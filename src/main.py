from PIL import Image
from generator import Generator, ShapeType

reference_img = Image.open("./assets/starry-night.png").convert("RGBA")

def main(iters: int):
    gen = Generator(reference_img, 100, ShapeType.TRIANGLE, 30)
    # for i, ind in enumerate(gen.individuals):
    #     ind.img.save(f"./generated/gen{gen.generation:02}/ind-{i:02}.png")
    last_fitness_check = 0
    while (last_fitness_check < 0.9 and iters > 0):
        gen.new_generation(5, 27)
        fittest = gen.fittest
        if (fittest.fitness - last_fitness_check > 0.01):
            last_fitness_check = fittest.fitness
            fittest.img.save(f"./generated/fittest-gen-{gen.generation:03}.png")

        # for i, ind in enumerate(gen.individuals):
        #     ind.img.save(f"./generated/gen{gen.generation:02}/ind-{i:02}.png")

        print(f"Gen {gen.generation:03} - Fitness: {fittest.fitness}")
        # print(f"Pop: {len(gen.individuals)}, il: {len(fittest.shapes)}")
        iters -= 1

import cProfile
import pstats

with cProfile.Profile() as pr:
    main(10)

stats = pstats.Stats(pr)
stats.strip_dirs()
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats(20)  # top 20 time-consuming calls
