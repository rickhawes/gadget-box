"""A feature to place a space in a feature layout."""

from dataclasses import dataclass
from typing import override

from gadget_box.core import Assembler, Feature, HolePattern, HolePatternBlock, Mm, Vec2


@dataclass
class Spacer(Feature):
    """A spacer fills space to help with the layout of a plate.

    A spacer can have specific minimum size through the `height`
    and `width` and be made expandable through`more_x` and
    `more_y` parameters. A spacer can have a hole pattern or
    be solid.

    """

    width: Mm = 0
    height: Mm = 0
    more_x: bool = False
    more_y: bool = False
    hole_pattern: HolePattern | None = None

    @override
    def desired_size(self) -> Feature.DesiredSize:
        return Feature.DesiredSize(
            Vec2(self.width, self.height), self.more_x, self.more_y
        )

    @override
    def render(self, asm: Assembler) -> None:
        if self.hole_pattern is not None:
            size = asm.plate_bx.size
            block = HolePatternBlock(size.x, size.y, size.z, self.hole_pattern)
            asm.place_block(block, cut=True)


class XSpacer(Spacer):
    """A spacer that expands horizontally."""

    def __init__(self, width: Mm = 0):
        super().__init__(width=width, more_x=True)


class YSpacer(Spacer):
    """A spacer that expands vertically."""

    def __init__(self, height: Mm = 0):
        super().__init__(height, more_y=True)
