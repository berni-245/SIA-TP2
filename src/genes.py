from typing import Tuple


class ColorGene:
    def __init__(self, rgba: int) -> None:
        if not (0 <= rgba <= 0xFFFFFFFF):
            raise ValueError("RGBA value must be a 32-bit integer (0 to 0xFFFFFFFF)")
        self.rgba = rgba

    @property
    def red(self) -> int:
        return (self.rgba >> 24) & 0xFF

    @property
    def green(self) -> int:
        return (self.rgba >> 16) & 0xFF

    @property
    def blue(self) -> int:
        return (self.rgba >> 8) & 0xFF

    @property
    def alpha(self) -> int:
        return self.rgba & 0xFF

    def __repr__(self) -> str:
        return f"ColorGene(R={self.red}, G={self.green}, B={self.blue}, A={self.alpha})"

# class ShapeGene:
#     def __init__(self) -> None:
#         pass
#

class TriangleGene:
    def __init__(self, vertices: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> None:
        self.vertices = vertices
