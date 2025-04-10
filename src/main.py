from PIL import Image

from generator import Generator, ShapeType

reference_img = Image.open("./assets/triangles.png").convert("RGBA")

gen = Generator(reference_img, 30, ShapeType.ELLIPSE, 5)

for i, indi in enumerate(gen.individuals):
    indi.img.save(f"./generated/test-ellipse-{i:02}.png")
