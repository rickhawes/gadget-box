from dataclasses import dataclass
from typing import final, override

from ..core.assembler import Assembler
from ..core.block import ExtrudedBlock, PlateBlock
from ..core.corners import SquareCorners
from ..core.feature import FeatureList
from ..core.figures import (
    AlignedFigure,
    CutoutFigure,
    RectangleFigure,
    RotatedFigure,
    TrapezoidFigure,
)
from ..core.geometry import Ax2, AxDir, AxDir3, Bx, Mm, Vec3
from ..core.hole_patterns import HexFill
from ..core.layouts import GridLayout, Layout
from ..core.model import Model
from .rack_dims import RackDims, ShelfTabDims, rack_units_to_mm
from .rack_holes import RackHolePattern


@final
class Shelf(Model):
    @dataclass(frozen=True)
    class Style:
        """
        Parameters for the style of the rack shelf.
        """

        base_thickness: Mm = 4.0
        """Thickness of the base of the rack shelf."""
        wall_thickness: Mm = 3.0
        """Thickness of the wall of the rack shelf."""
        face_thickness: Mm = 3.0
        """Thickness of the face of the rack shelf."""
        face_rounding: Mm = 3.0
        """Rounding of the face of the rack shelf."""
        shelf_depth: Mm = RackDims.DEPTH_8INCH
        """Whether the rack shelf has a ten inch depth."""
        shelf_back_depth: float = 20
        """The back of the shelf has a small inset."""
        open_face: bool = True
        """Whether the face of the rack shelf is open or closed."""
        middle_holes: bool = True
        """Whether the rack shelf plate has middle holes."""
        half_height_bottom: bool = False
        """Whether the rack shelf plate has half-height bottom holes."""

    OPEN_FACE = Style(open_face=True)
    """A rack shelf with an open face."""

    CLOSE_FACE = Style(open_face=False)
    """A rack shelf with a closed face."""

    def __init__(
        self,
        rack_units: float = 1.0,
        style: Style = OPEN_FACE,
        shelf_features: FeatureList | None = None,
        shelf_layout: Layout | None = None,
    ):
        """
        A rack shelf with either an open or closed face.

        Args:
            rack_units: The number of rack units the shelf spans.
            style: The style of the rack shelf.
            shelf_features: The features to add to the rack shelf.
            shelf_layout: The layout of the rack shelf.
        """
        self.rack_units = rack_units
        self.style = style
        self.shelf_features = shelf_features
        self.shelf_layout = shelf_layout if shelf_layout is not None else GridLayout()
        assert 4 * style.shelf_back_depth < style.shelf_depth, (
            "wall_inset must be less than shelf_depth / 4"
        )

    @override
    def render(self) -> Model.Rendering:
        # geometry
        plate_size = Vec3(
            RackDims.SHELF_WIDTH,
            self.style.shelf_depth,
            self.style.base_thickness,
        )
        exterior_dz = rack_units_to_mm(self.rack_units)
        exterior_bx = Bx(plate_size.x, plate_size.y, exterior_dz, 0, 0, exterior_dz / 2)
        interior_dz = rack_units_to_mm(self.rack_units) - plate_size.z
        interior_dx = plate_size.x - 2 * self.style.wall_thickness
        interior_bx = Bx(interior_dx, plate_size.y, interior_dz, 0, 0, interior_dz / 2)

        # wall
        def build_walls() -> None:
            # Make a wall block that is a combination of figures
            wall_size = Vec3(plate_size.y, interior_dz, self.style.wall_thickness)
            shelf_back = self.style.shelf_back_depth
            wall_back = RectangleFigure(shelf_back, 2 * plate_size.z)
            wall_trap = TrapezoidFigure(
                wall_size.y,
                wall_size.x / 2 - shelf_back,
                angle1=90,
                minor_width=2 * plate_size.z,
            )
            wall_trap = RotatedFigure(wall_trap, angle=90)
            wall_holes = RectangleFigure(
                wall_size.x / 2,
                wall_size.y,
                holes=HexFill(),
                corners=SquareCorners(wall_size.z),  # insets the fill area a bit
            )
            wall_figure = AlignedFigure([wall_back, wall_trap, wall_holes], Ax2.X, AxDir.MINUS)
            wall = ExtrudedBlock(wall_figure, wall_size.z)

            # Place the walls on the plate
            wall_plate_bx_minus = interior_bx.side_bx(AxDir3.X_MINUS)
            wall_plate_bx_plus = wall_plate_bx_minus.move(
                Vec3(interior_bx.size.x + wall_size.z, 0, 0)
            )
            for plate_bx in [wall_plate_bx_minus, wall_plate_bx_plus]:
                wall_sub = plate_asm.make_sub(plate_bx, AxDir3.X_MINUS)
                wall_sub.place_block(wall)

        # add face
        def build_faceplate(base_asm: Assembler) -> None:
            size = Vec3(RackDims.WIDTH_10INCH, exterior_dz, self.style.face_thickness)
            holes = RackHolePattern(self.rack_units)
            figure = RectangleFigure(size.x, size.y, self.style.face_rounding, holes)
            if self.style.open_face:
                open_dx = ShelfTabDims.MAX_DX_TABS - 2 * self.style.wall_thickness
                figure = CutoutFigure(figure, RectangleFigure(open_dx, size.y))
            face = ExtrudedBlock(figure, size.z)
            sub = base_asm.make_sub(exterior_bx, AxDir3.Y_MINUS)
            sub.place_block(face)

        # shelf
        asm = Assembler.make(exterior_bx.side_bx(AxDir3.BOTTOM))
        build_faceplate(asm)
        plate = PlateBlock(plate_size.x, plate_size.y, plate_size.z)
        plate_asm = asm.stack_block(plate)
        build_walls()
        build_faceplate(asm)
        if self.shelf_features is not None:
            self.shelf_layout.render_features(self.shelf_features, asm)

        return asm.make_rendering()
