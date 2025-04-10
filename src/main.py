from PIL import Image, ImageChops
import numpy as np

from generator import Generator, ShapeType

# Value closer to 0 is more similar.
def compare_images(img1, img2):
    if img1.size != img2.size:
        raise ValueError("Images must have the same dimensions.")

    diff = ImageChops.difference(img1, img2)
    np_diff = np.array(diff)

    return np.mean(np_diff)

reference_img = Image.open("./assets/triangles.png").convert("RGBA")

gen = Generator(reference_img, 30, ShapeType.TRIANGLE, 10)

for i, indi in enumerate(gen.individuals):
    indi.img.save(f"./generated/test-{i:02}.png")

# Compare
# similarity = compare_images(indi.img, reference_img)
# print(f"Similarity: {similarity}")
