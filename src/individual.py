import cairo
from typing import List, Tuple
from PIL import Image
from skimage.color import rgb2lab
from src.genes import Shape

class Individual:
    current_id: int = 1
    def __init__(self, shapes: List[Shape], img_size: Tuple[int, int]) -> None:
        self.shapes = shapes
        self.shape_count = len(shapes)
        self.id = Individual.current_id
        Individual.current_id += 1

        width, height = img_size
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self.surface)

        for shape in self.shapes:
            shape.draw(ctx)

        self.img = self._cairo_to_img()
        # Uncomment the lines below if you want to use the delta_D fitness
        # rgb = np.asarray(self.img.convert("RGB")) / 255.0
        # self.lab = rgb2lab(rgb)
        self.fitness = -1


    def set_fitness(self, fitness: float):
        self.fitness = fitness

    def _cairo_to_img(self) -> Image.Image:
        buf = self.surface.get_data()
        width = self.surface.get_width()
        height = self.surface.get_height()

        # Convert Cairo surface (BGRA) to Pillow image (RGBA)
        return Image.frombuffer("RGBA", (width, height), buf.tobytes(), "raw", "BGRA", 0, 1)
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Individual) and value.id == self.id
    
    def __hash__(self) -> int:
        return hash(self.id)

