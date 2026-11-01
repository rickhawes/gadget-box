"""
2d Elements for models. Elements are the primitives that make up models and parts. They are built to be easily combined and rendered.
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence, override

from build123d import (
    BuildLine,
    BuildSketch,
    Circle,
    Face,
    Line,
    Location,
    Mode,
    Polyline,
    Rectangle,
    RectangleRounded,
    Sketch,
    SlotOverall,
    Trapezoid,
    make_face,
    offset,
)

from .corners import Corners, RoundedCorners, SquareCorners
from .geometry import Ax2, AxDir, Degree, Mm, Rc, Vec2
from .hole_patterns import HolePattern
from .print_dims import E

#
# region Base classes
#


@dataclass(frozen=True)
class Op2:
    figure: Figure
    """Figure to combine"""
    pos: Vec2 = Vec2(0, 0)
    """offset the figure"""
    angle: Degree = 0
    """rotate the figure"""
    cut: bool = False
    """cut (i.e. subtract) the figure"""

    def to_location(self) -> Location:
        return Location((self.pos.y, self.pos.y), angle=self.angle)

    def to_mode(self) -> Mode:
        return Mode.SUBTRACT if self.cut else Mode.ADD

    def to_bounds(self) -> Rc:
        """Return the bounding rectangle of the shape with the given `op`"""
        sin = math.sin(math.radians(self.angle))
        cos = math.cos(math.radians(self.angle))
        size = self.figure.size
        dx = abs(size.y * sin + size.x * cos)
        dy = abs(size.y * cos + size.x * sin)
        return Rc(Vec2(dx, dy), self.pos)


class Figure(ABC):
    """ABC for the 2d shapes that are used to form 3d shapes."""

    @property
    @abstractmethod
    def size(self) -> Vec2:
        """Returns the size of the shape in 2d without any rotation"""

    @abstractmethod
    def sketch(self) -> Sketch:
        """Draw the outline of the shape according to the `op` ignoring the `op.element` field."""


# endregion

#
# region Specific elemental figures
#


class CircleFigure(Figure):
    """A circle figure with a `radius`."""

    radius: Mm

    def __init__(self, radius: Mm) -> None:
        """
        Args:
            radius (Mm): The radius of the circle.
        """
        self.radius = radius

    @property
    @override
    def size(self) -> Vec2:
        return Vec2(2 * self.radius, 2 * self.radius)

    @override
    def sketch(self) -> Sketch:
        return Circle(self.radius)


class RectangleFigure(Figure):
    """A rectangle shape or rounded rectangle shape."""

    width: Mm
    height: Mm
    corners: Corners
    holes: HolePattern | None

    def __init__(
        self,
        width: Mm,
        height: Mm,
        corners: Mm | Corners | None = None,
        holes: HolePattern | None = None,
    ) -> None:
        """
        Args:
            width (Mm): The width of the rectangle.
            height (Mm): The height of the rectangle.
            corners (Corners): The corner shape of the rectangle.
                If a `Mm` > 0, then a Rounded Corner is used.
            holes (HolePattern): The hole pattern for the inside of the rectangle after
                insetting the rectangle for the corner size. Defaults to Fill.SOLID.
        """
        self.width = width
        self.height = height
        if isinstance(corners, (int, float)):
            self.corners = RoundedCorners(corners)
        elif corners is None:
            self.corners = SquareCorners(0)
        else:
            self.corners = corners
        self.holes = holes

    @property
    @override
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    @override
    def sketch(self) -> Sketch:
        def solid_fill() -> Sketch:
            """Sketch the rectangle with its corners"""
            # Optimize for square and rounded corners
            match self.corners:
                case SquareCorners():
                    return Rectangle(self.width, self.height)
                case RoundedCorners() if self.corners.radius == 0:
                    return Rectangle(self.width, self.height)
                case RoundedCorners():
                    return RectangleRounded(self.width, self.height, self.corners.radius)
                case _:
                    return complex_corners()

        def complex_corners() -> Sketch:
            cs = self.corners.size
            cw, ch = cs.x, cs.y
            dx, dy = (self.width / 2) - cw, (self.height / 2) - ch
            with BuildSketch() as sk:
                with BuildLine():
                    # side lines
                    l_top = Line((-dx, dy + ch), (dx, dy + ch))
                    l_right = Line((dx + cw, dy), (dx + cw, -dy))
                    l_bottom = Line((dx, -dy - ch), (-dx, -dy - ch))
                    l_left = Line((-dx - cw, -dy), (-dx - cw, dy))
                    # corners
                    self.corners.draw(l_top @ 1, l_right @ 0, Corners.TOP_RIGHT)
                    self.corners.draw(l_right @ 1, l_bottom @ 0, Corners.BOTTOM_RIGHT)
                    self.corners.draw(l_bottom @ 1, l_left @ 0, Corners.BOTTOM_LEFT)
                    self.corners.draw(l_left @ 1, l_top @ 0, Corners.TOP_LEFT)
                _ = make_face()
            return Sketch(sk.sketch)

        def hole_fill() -> Sketch:
            assert self.holes is not None, "fill must be provided"

            # make a sketch of the holes
            #
            outline = solid_fill().wire()
            holes = self.holes.locations(self.size, self.corners.size) * self.holes.sketch().wire()
            sk = Sketch()
            sk += Face(outline, holes)
            return sk

        if self.holes is None:
            return solid_fill()
        else:
            return hole_fill()


class SlotFigure(Figure):
    """A slot shape."""

    width: Mm
    height: Mm

    def __init__(self, width: Mm, height: Mm) -> None:
        """
        Args:
            width (Mm): The width of the slot.
            height (Mm): The height of the slot.
        """
        self.width = width
        self.height = height

    @property
    @override
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    @override
    def sketch(self) -> Sketch:
        return SlotOverall(self.width, self.height)


class TrapezoidFigure(Figure):
    """A trapezoid shape with the major width on the bottom and minor on the top."""

    width: Mm
    height: Mm
    angle1: float
    angle2: float | None = None
    minor_width: Mm | None = None

    def __init__(
        self,
        width: Mm,
        height: Mm,
        angle1: float | None = 90,
        angle2: float | None = None,
        minor_width: Mm | None = None,
    ) -> None:
        """
        A trapezoid shape with the major width on the bottom and minor on the top.

        Args:
            width (Mm): The major width of the trapezoid.
            height (Mm): The height of the trapezoid.
            angle1 (Mm): The interior angle of the first side. Defaults to 90.
            angle2 (Mm): The interior angle of the second side. Defaults to angle1.
            minor_width (Mm): The width of the minor side. Defaults to None.
        """
        if angle1 is not None and angle2 is not None and minor_width is not None:
            raise ValueError("angle1, angle2, and minor_width cannot all be set")
        if angle1 is None and angle2 is None and minor_width is None:
            raise ValueError("angle1, angle2, and minor_width cannot all be None")

        if minor_width is not None:
            # Calculate angle1 or angle2 based on minor_width
            if angle1 is not None and angle2 is None:
                reduction_left = 0 if angle1 == 90 else height / math.tan(math.radians(angle1))
                angle2 = math.degrees(math.atan(height / (width - minor_width - reduction_left)))
            elif angle1 is None and angle2 is not None:
                reduction_right = 0 if angle2 == 90 else height / math.tan(math.radians(angle2))
                angle1 = math.degrees(math.atan(height / (width - minor_width - reduction_right)))
            else:
                angle1 = angle2 = math.degrees(math.atan(2 * height / (width - minor_width)))
        if angle2 is not None and angle1 is None:
            angle1 = angle2
        assert angle1 is not None, "angle1 could not be calculated"

        self.width = width
        self.height = height
        self.angle1 = angle1
        self.angle2 = angle2

    @property
    @override
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    @override
    def sketch(self) -> Sketch:
        return Trapezoid(
            self.width, self.height, left_side_angle=self.angle1, right_side_angle=self.angle2
        )


class TriangleFigure(Figure):
    """A triangle shape, by default it is an iso-triangle"""

    width: Mm
    height: Mm
    tip_ratio: float

    def __init__(self, width: Mm, height: Mm, tip_ratio: float = 0.0) -> None:
        """
        Args:
            width (Mm): The width of the triangle.
            height (Mm): The height of the triangle.
        """
        self.width = width
        self.height = height
        self.tip_ratio = tip_ratio

    @property
    @override
    def size(self) -> Vec2:
        return Vec2(max(self.width, abs(self.tip_ratio * self.width / 2)), self.height)

    @override
    def sketch(self) -> Sketch:
        dx, dy = self.width / 2, self.height / 2
        tip_x = self.tip_ratio * dx
        pts = [(-dx, -dy), (tip_x, dy), (dx, -dy)]
        return make_face(Polyline(pts, close=True))


# endregion

#
# region Figures that combine other figures together
#


class CombinedFigure(Figure):
    ops: Sequence[Op2]

    def __init__(self, ops: Sequence[Op2]) -> None:
        self.ops = ops

    @override
    @property
    def size(self) -> Vec2:
        return Rc.union(*(op.to_bounds() for op in self.ops)).size

    @override
    def sketch(self) -> Sketch:
        # TODO: Reduce fusing operations by combining runs of single modes together first
        sk = Sketch()
        for op in self.ops:
            if op.cut:
                sk = Sketch(
                    sk - (Location(op.pos.to_vector(), angle=op.angle) * op.figure.sketch())
                )
            else:
                sk = Sketch(sk + Location(op.pos.to_vector(), angle=op.angle) * op.figure.sketch())
        return Sketch(sk)


class AlignedFigure(CombinedFigure):
    """A combined figure with all the figures aligned along an axis."""

    axis: Ax2
    align: AxDir

    def __init__(
        self, figures: Sequence[Figure], axis: Ax2 = Ax2.X, align: AxDir = AxDir.CENTER
    ) -> None:
        self.axis = axis
        self.align = align

        fig_rcs = [Rc(fig.size) for fig in figures]
        arranged_rcs = Rc.arrange(axis, align, *fig_rcs)
        fig_ops = [Op2(fig, rc.center) for rc, fig in zip(arranged_rcs, figures)]
        super().__init__(fig_ops)


class CutoutFigure(CombinedFigure):
    """Create an element that has a `base` with a `cutout` elements"""

    base: Figure
    cutout: Figure

    def __init__(self, base: Figure, cutout: Figure) -> None:
        fig_ops = [Op2(base), Op2(cutout, cut=True)]
        super().__init__(fig_ops)
        self.base = base
        self.cutout = cutout


class OutsetFigure(Figure):
    """Create an element that is a `base` element that is outset by `amount`"""

    base: Figure
    """The base shape"""
    outset: Mm
    """The outset amount (may be negative for an inset)"""

    def __init__(self, base: Figure, outset: Mm) -> None:
        if abs(outset) < E:
            raise ValueError("outset must not be 0")
        self.base = base
        self.outset = outset

    @override
    @property
    def size(self) -> Vec2:
        return (
            self.base.size
            if self.outset < 0
            else self.base.size + Vec2(2 * self.outset, 2 * self.outset)
        )

    @override
    def sketch(self) -> Sketch:
        base = self.base.sketch()
        return Sketch(offset(base, self.outset))


class RotatedFigure(Figure):
    """Create an figure that is a `base` rotated by `angle`"""

    base: Figure
    """The base shape"""
    angle: Degree
    """The outset amount (may be negative for an inset)"""
    _op2: Op2

    def __init__(self, base: Figure, angle: Degree) -> None:
        self.base = base
        self.angle = angle
        self._op2 = Op2(base, angle=angle)

    @override
    @property
    def size(self) -> Vec2:
        return self._op2.to_bounds().size

    @override
    def sketch(self) -> Sketch:
        return self._op2.to_location() * self.base.sketch()


class RingFigure(CombinedFigure):
    """Create a figure that is a ring of a `base` figure."""

    base: Figure
    outset: Mm

    def __init__(self, base: Figure, outset: Mm) -> None:
        outset_fig = OutsetFigure(base, outset)
        outer, inner = (outset_fig, base) if outset > 0 else (base, outset_fig)
        fig_ops = [Op2(outer), Op2(inner, cut=True)]
        super().__init__(fig_ops)
        self.base = base
        self.outset = outset


# endregion
