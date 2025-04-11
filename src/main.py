from PIL import Image

from generator import Generator, ShapeType

reference_img = Image.open("./assets/franco.png").convert("RGBA")

gen = Generator(reference_img, 5, ShapeType.TRIANGLE, 5)

for _ in range(4):
    gen.trad_generational_jump()

for i, indi in enumerate(gen.individuals):
    indi.img.save(f"./generated/test-ellipse-{i:02}.png")
