from typing import List
from PIL import Image, ImageChops
import numpy as np

from genes import Elipse, Shape, Triangle
from individual import Individual

# Value closer to 0 is more similar.
def compare_images(img1, img2):
    if img1.size != img2.size:
        raise ValueError("Images must have the same dimensions.")

    diff = ImageChops.difference(img1, img2)
    np_diff = np.array(diff)

    return np.mean(np_diff)

reference_img = Image.open("./assets/triangles.png").convert("RGBA")

triangles: List[Shape] = [
    Triangle((255, 120,   0, 255), (( 0,   0), ( 20,   0), (  0,  20))),
    Triangle((255, 255, 100, 128), (( 0,   0), ( 30,   0), (  0,  10))),
    Triangle((255,   0,   0, 128), ((50, 100), (200, 100), (150, 150))),
    Triangle((  0, 120, 255, 250), ((30,  30), (  0,  50), ( 90, 90))),
    Elipse((  255, 120, 255, 100), (30,  30), (  50,  100)),
]
i1 = Individual(triangles, reference_img.size)
i1.img.save("./generated/test.png")


# Compare
similarity = compare_images(i1.img, reference_img)
print(f"Similarity: {similarity}")
