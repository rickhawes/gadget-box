"""Holes that go through the plate."""

from enum import Enum
from typing import Sequence, override

from gadget_box.core import Assembler, CylinderBlock, Feature, Mm, Vec2


class StandardScrewDiameters(float, Enum):
    """Standard screw hole diameters"""

    M2 = 2.1
    M3 = 3.1
    M4 = 4.1
    M5 = 5.1
    M6 = 6.1


class MultipleHoles(Feature):
    """Multple through holes"""

    _pattern: list[Vec2]
    """The locations of the holes relative to the center"""
    _pattern_size: Vec2
    """The size of the pattern."""
    hole_diameter: Mm
    """The hole diameter."""

    def __init__(self, locations: Sequence[Vec2], hole_diameter: Mm) -> None:
        # compute the min and max of the locations to center the holes
        min_x = min(l.x for l in locations)
        max_x = max(l.x for l in locations)
        min_y = min(l.y for l in locations)
        max_y = max(l.y for l in locations)
        center = Vec2((min_x + max_x) / 2, (min_y + max_y) / 2)
        self._pattern_size = Vec2(max_x - min_x, max_y - min_y)
        self._pattern = [l - center for l in locations]
        self.hole_diameter = hole_diameter

    @override
    def desired_size(self) -> Feature.DesiredSize:
        size = self._pattern_size + Vec2(self.hole_diameter, self.hole_diameter)
        return Feature.DesiredSize(min_size=size)

    @override
    def render(self, asm: Assembler) -> None:
        hole = CylinderBlock(self.hole_diameter / 2, asm.plate_depth)
        places = [Assembler.Place(offset=l) for l in self._pattern]
        asm.place_block(hole, places, cut=True)


class FourHoles(MultipleHoles):
    """4 holes at the corners of a rectangle."""

    def __init__(self, width: Mm, height: Mm, hole_diameter: Mm) -> None:
        dx, dy = width / 2, height / 2
        pattern = [Vec2(-dx, -dy), Vec2(-dx, dy), Vec2(dx, -dy), Vec2(dx, dy)]
        super().__init__(pattern, hole_diameter)
