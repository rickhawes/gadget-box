from dataclasses import dataclass

from mini_rack_printables import HolePattern

from ..core.assembler import Assembler
from ..core.corners import InsetCorners
from ..core.elements_3d import PlateElement, PrismElement, StackElement
from ..core.feature import Feature, Rib
from ..core.figures import CutoutFigure, OutsetFigure, RectangleFigure, RingFigure
from ..core.geometry import AxDir3, Bx, Dir2, Mm, Vec2, Vec3
from ..core.hole_patterns import HexFill


@dataclass(frozen=True)
class BasicHolderStyle:
    """
    Represents the style a style
    """

    outer_radius: Mm = 0.0
    inner_radius: Mm = 0.0
    wall_thickness: Mm = 2.5
    corner_edge: Mm = 1.0
    holes: HolePattern | None = HexFill()


def build_basic_holder(
    asm: Assembler, device_size: Vec3, style: BasicHolderStyle = BasicHolderStyle()
) -> None:
    # geometry
    dx, dy, dz = device_size.to_tuple()
    cr = style.outer_radius
    w = style.wall_thickness
    ir = style.inner_radius
    e = style.corner_edge  # corner edge
    dc = ir + e  # corner width

    # add corners
    corners = PrismElement(
        CutoutFigure(
            base=CutoutFigure(
                RectangleFigure(dx + 2 * w, dy + 2 * w, cr), RectangleFigure(dx, dy, ir)
            ),
            cutout=RectangleFigure(dx + 2 * w, dy + 2 * w, InsetCorners(dc + w)),
        ),
        dz,
    )
    asm.place_element(corners)

    # add walls
    # build around a box defined by the device
    device_bx = asm.place_bounds(size=Vec3(dx, dy, dz))
    for side in [AxDir3.X_PLUS, AxDir3.X_MINUS, AxDir3.Y_PLUS, AxDir3.Y_MINUS]:
        plate_sub = asm.make_sub(device_bx, side)
        size = device_bx.side_size(side) - Vec2(2 * dc, 0)
        block = PlateElement(size.x, size.y, w, holes=style.holes)
        plate_sub.place_element(block)
