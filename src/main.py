from PIL import Image, ImageDraw, ImageChops
import numpy as np

def draw_triangles_pillow(coord_triplets, colors, size=(300, 300), background=(255, 255, 255, 0)):
    img = Image.new("RGBA", size, background)
    draw = ImageDraw.Draw(img, "RGBA")

    for vertices, color in zip(coord_triplets, colors):
        draw.polygon(vertices, fill=color)

    return img

# Value closer to 0 is more similar.
def compare_images(img1, img2):
    if img1.size != img2.size:
        raise ValueError("Images must have the same dimensions.")

    diff = ImageChops.difference(img1, img2)
    np_diff = np.array(diff)

    return np.mean(np_diff)

# Example usage:

# Triangle data
coords = [
    [(50, 50), (150, 50), (100, 130)],
    [(160, 60), (210, 40), (200, 100)]
]

colors = [
    (255, 0, 0, 128),  # semi-transparent red
    (0, 255, 0, 255)   # solid green
]

# Load reference image
reference = Image.open("./assets/triangles.png").convert("RGBA")

# Draw and save generated image
generated = draw_triangles_pillow(coords, colors, reference.size)
generated.save("./generated/test.png")


# Compare
similarity = compare_images(generated, reference)
print(f"Similarity: {similarity}")
