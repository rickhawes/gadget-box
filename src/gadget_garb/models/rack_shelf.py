"""A 10-inch rack shelf model."""

from dataclasses import dataclass
from typing import ClassVar

from gadget_garb.core import (
    AlignedFigure,
    Assembler,
    Ax2,
    AxDir,
    AxDir3,
    Bx,
    CutoutFigure,
    Dir2,
    ExtrudedBlock,
    FeatureList,
    GridLayout,
    HexFill,
    HolePattern,
    Layout,
    Mm,
    PlateBlock,
    Rc,
    RectangleFigure,
    Rendering,
    RotatedFigure,
    RowLayout,
    SquareCorners,
    TrapezoidFigure,
    Vec2,
    Vec3,
)

from .rack_dims import RackDims, ShelfTabDims, rack_units_to_mm
from .rack_holes import RackHolePattern


@dataclass(frozen=True)
class ShelfStyle:
    """
    Parameters for the style of the rack shelf.
    """

    @dataclass(frozen=True)
    class Face:
        """The face sytle."""

        is_open: bool = True
        """Whether the face of the rack shelf is open or closed."""
        middle_holes: bool = True
        """Whether the rack shelf plate has middle holes."""
        half_height_bottom: bool = False
        """Whether the rack shelf plate has half-height bottom holes."""
        thickness: Mm = 3.0
        """Thickness of the face of the rack shelf."""
        rounding: Mm = 3.0
        """Rounding of the face of the rack shelf."""
        feature_inset: Vec2 = Vec2(3.0, 0.0)
        """The amount of inset for features."""
        layout: Layout = RowLayout()
        """The layout of the faceplate"""

    @dataclass(frozen=True)
    class Base:
        """The style for the base."""

        thickness: Mm = 4.0
        """Thickness of the base of the rack shelf."""
        depth: Mm = RackDims.DEPTH_8INCH
        """Whether the rack shelf has a ten inch depth."""
        back_inset: float = 20
        """The back of the shelf has a small inset."""
        layout: Layout = GridLayout()
        """The layout of the base plate"""

    @dataclass(frozen=True)
    class Wall:
        """The style for the walls"""

        thickness: Mm = 3.0
        """Thickness of the wall of the rack shelf."""
        hole_pattern: HolePattern | None = HexFill()

    face: Face = Face()
    """Style elements for the face of the shelf."""
    base: Base = Base()
    """Style elements for the base of the shelf."""
    wall: Wall = Wall()
    """Style elements for the walls of the shelf."""

    OPEN_FACE: ClassVar["ShelfStyle"]
    """A rack shelf with an open face."""

    CLOSE_FACE: ClassVar["ShelfStyle"]
    """A rack shelf with a closed face."""


ShelfStyle.OPEN_FACE = ShelfStyle(face=ShelfStyle.Face(is_open=True))
ShelfStyle.CLOSE_FACE = ShelfStyle(face=ShelfStyle.Face(is_open=False))


def render_rack_shelf(
    rack_units: float = 1.0,
    style: ShelfStyle = ShelfStyle.OPEN_FACE,
    base_features: FeatureList | None = None,
    face_features: FeatureList | None = None,
) -> Rendering:
    """Render a rack shelf

    Args:
        rack_units (float): The number of rack units the shelf spans.
        style (ShelfStyle): The style of the rack shelf.
        features (FeatureList): The features to add to the rack shelf.
        layout (Layout): The layout of the rack shelf. Default is GridLayout.

    Returns:
        Rendering of a rack shelf.
    """
    # Normalize args
    if face_features is not None and style.face.is_open:
        raise ValueError("Cannot have a open face style with face features.")

    # geometry
    plate_size = Vec3(
        RackDims.SHELF_WIDTH,
        style.base.depth,
        style.base.thickness,
    )
    exterior_dz = rack_units_to_mm(rack_units)
    exterior_bx = Bx(plate_size.x, plate_size.y, exterior_dz, 0, 0, exterior_dz / 2)
    interior_dz = rack_units_to_mm(rack_units) - plate_size.z
    interior_dx = plate_size.x - 2 * style.wall.thickness
    interior_bx = Bx(interior_dx, plate_size.y, interior_dz, 0, 0, interior_dz / 2)

    # wall
    def build_walls(plate_asm: Assembler) -> None:
        """Add walls to the left and right top of the base."""
        # Make a wall block that is a combination of figures
        wall_size = Vec3(plate_size.y, interior_dz, style.wall.thickness)
        shelf_back = style.base.back_inset
        wall_back = RectangleFigure(shelf_back, 2 * plate_size.z)
        wall_trap = TrapezoidFigure(
            wall_size.y,
            wall_size.x / 2 - shelf_back,
            angle1=90,
            angle2=TrapezoidFigure.angle_from_widths(
                wall_size.y, 2 * plate_size.z, wall_size.x / 2 - shelf_back, angle1=90
            ),
        )
        wall_trap = RotatedFigure(wall_trap, angle=90)
        wall_holes = RectangleFigure(
            wall_size.x / 2,
            wall_size.y,
            corners=SquareCorners(wall_size.z),
            holes=style.wall.hole_pattern,
        )
        wall_figure = AlignedFigure(
            [wall_back, wall_trap, wall_holes], Ax2.X, AxDir.MINUS
        )
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
    def build_faceplate(base_asm: Assembler, face_features: FeatureList | None) -> None:
        """Add the faceplate to the exterior-bottom assembler"""
        size = Vec3(RackDims.WIDTH_10INCH, exterior_dz, style.face.thickness)

        # build the faceplate block with rack holes
        holes = RackHolePattern(rack_units)
        figure = RectangleFigure(
            size.x, size.y, corners=style.face.rounding, holes=holes
        )
        open_dx = ShelfTabDims.MAX_DX_TABS - 2 * style.wall.thickness
        if style.face.is_open:
            figure = CutoutFigure(figure, RectangleFigure(open_dx, size.y))
        face = ExtrudedBlock(figure, size.z)

        # position the block
        plane_bx = base_asm.place_bx(
            Vec3(size.x, 0, size.y), Assembler.Place(Dir2.Y_MINUS, Vec2(0, -size.z))
        )
        face_sub = base_asm.make_sub(plane_bx, AxDir3.Y_PLUS)
        feature_sub = face_sub.stack_block(face)
        if face_features is not None:
            # work in base coordinates
            area = Rc(
                open_dx - 2 * style.face.feature_inset.x,
                size.y - 2 * style.base.thickness - 2 * style.face.feature_inset.y,
            )
            style.face.layout.render_features(face_features, feature_sub, area=area)

    # shelf
    bottom_asm = Assembler.make(exterior_bx.side_bx(AxDir3.BOTTOM))
    plate = PlateBlock(plate_size.x, plate_size.y, plate_size.z)
    plate_asm = bottom_asm.stack_block(plate)
    if base_features is not None:
        style.base.layout.render_features(base_features, plate_asm)

    build_walls(plate_asm)
    build_faceplate(bottom_asm, face_features)

    return bottom_asm.make_rendering()
