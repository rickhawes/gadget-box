"""
A device holder for a single device on a shelf. Devices are held by
friction from the corners. The corners are cut out of a rounded rect or
a general device shape.
"""

from dataclasses import dataclass
from typing import override

from ..core.assembler import Assembler
from ..core.block import ExtrudedBlock
from ..core.corners import Corners, InsetCorners
from ..core.feature import Feature
from ..core.figures import CutoutFigure, Figure, RectangleFigure, RingFigure
from ..core.geometry import Mm, Vec2


class GeneralCornerHolder(Feature):
    """
    A corner holder for a general shape.
    """

    shape: Figure
    opening: Vec2
    style: GeneralCornerHolder.Style

    @dataclass(frozen=True)
    class Style:
        """Style for the holder"""

        thickness: Mm = 3.0
        """Corner wall thickness"""
        height: Mm = 5.0
        """Corner height"""

    def __init__(
        self,
        shape: Figure,
        opening: Vec2 = Vec2(-10.0, -10.0),
        style: GeneralCornerHolder.Style = Style(),
    ) -> None:
        """
        Initialize a holder with the given style, device size, and

        Args:
            shape (Figure): The shape of the device to hold.
            opening (Vec2): The size of the opening in Mm
                or the size of corner extra if negative.
            style (Style): The style of the corners.
        """
        self.shape = shape
        self.opening = opening
        self.style = style

    @override
    def desired_size(self) -> Feature.DesiredSize:
        size = self.shape.size + Vec2(self.style.thickness, self.style.thickness) * 2
        return Feature.DesiredSize(size, False)

    @override
    def render(self, asm: Assembler) -> None:
        # dimensions
        w, d = self.style.thickness, self.style.height
        size = self.shape.size
        if self.opening.x > 0:
            cross_dx = (size.x - self.opening.x) / 2
        else:
            cross_dx = -self.opening.x
        if self.opening.y > 0:
            cross_dy = (size.y - self.opening.y) / 2
        else:
            cross_dy = -self.opening.y

        # sketch the holder shape
        cross = RectangleFigure(
            size.x + 2 * w,
            size.y + 2 * w,
            InsetCorners(cross_dx + 2 * w, cross_dy + 2 * w),
        )
        holder = RingFigure(self.shape, w)
        co = CutoutFigure(holder, cross)
        asm.place_block(ExtrudedBlock(co, d))


class CornerHolder(GeneralCornerHolder):
    """A a corner holder for a round rect device."""

    def __init__(
        self,
        width: Mm,
        height: Mm,
        corners: Corners | float | int | None = None,
        opening: Vec2 = Vec2(-15, -15),
        style: GeneralCornerHolder.Style = GeneralCornerHolder.Style(),
    ) -> None:
        """
        Initialize

        Args:
            width: Rectangle width
            height: Rectangle width
            opening: Opening amount
            corner: Specify the corner of the rectangle
        """
        super().__init__(RectangleFigure(width, height, corners), opening, style)
