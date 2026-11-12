"""A Facplate model for a 10-inch rack."""

from dataclasses import dataclass
from typing import ClassVar

from ..core.assembler import Assembler
from ..core.block import ExtrudedBlock, PlateBlock
from ..core.feature import FeatureList, Rib
from ..core.figures import TrapezoidFigure
from ..core.geometry import AxDir3, Dir2, Mm, Rc, Vec2, Vec3
from ..core.layouts import Layout, RowLayout
from ..core.rendering import Rendering
from .rack_dims import RackDims, ShelfTabDims
from .rack_holes import RackHolePattern


@dataclass(frozen=True)
class FaceplateStyle:
    """Style parameters for a faceplate"""

    thickness: Mm = 3.0
    """Thickness of the plate"""
    rounding: Mm = 3.0
    """Rounding applied to corners of a face_plate"""
    middle_holes: bool = True
    """Draw middle screw holes"""
    half_height_bottom: bool = False
    """Start the bottom with a half unit"""
    rib: Rib = Rib(2.0, 1.0)
    """Rib size for the plate"""
    layout: Layout = RowLayout()
    """The layout of the face plate."""

    PLAIN: ClassVar["FaceplateStyle"]
    """Plain or default style"""

    WITH_RIB: ClassVar["FaceplateStyle"]
    """With Rib style"""

    STD_RIB: ClassVar["Rib"]
    """The rib size that the faceplate uses."""


FaceplateStyle.STD_RIB = Rib(2.0, 1.0)
FaceplateStyle.PLAIN = FaceplateStyle()
FaceplateStyle.WITH_RIB = FaceplateStyle(rib=FaceplateStyle.STD_RIB)


def render_rack_faceplate(
    rack_units: float,
    style: FaceplateStyle = FaceplateStyle.PLAIN,
    features: FeatureList | None = None,
) -> Rendering:
    """
    Render the faceplate according to the parameters.

    Args:
        rack_units (float): the height of the plate in rack units.
        style (FaceplateSytle): the sytle used to render the plate,
            with PLAIN as the default.
        features (FeatureList): the features to place on the plate.
        layout (Layout): the layout to use for features. Default is
            RowLayout.

    Returns:
        A rendering of the faceplate.
    """
    plate_size = Vec2(RackDims.WIDTH_10INCH, rack_units * RackDims.HEIGHT_1U)
    feature_area = Rc(ShelfTabDims.MAX_DX_TABS, plate_size.y - 2 * style.rib.width)

    # form a round-rect base with cutout for the holes of the rack screws
    base = PlateBlock(
        plate_size.x,
        plate_size.y,
        style.thickness,
        corners=style.rounding,
        holes=RackHolePattern(rack_units, style.middle_holes, style.half_height_bottom),
    )

    # create an assembler to place the other blocks
    asm = Assembler.make_with_block(base)

    # ribs
    if style.rib is not None:

        def add_rib(dir2: Dir2) -> None:
            rib_size = Vec3(feature_area.size.x, style.rib.width, style.rib.depth)
            rib_bx = asm.place_bx(rib_size, Assembler.Place(origin=dir2))
            # place the sub assembly on the side
            rib_plane_bx = rib_bx.side_bx(AxDir3.Y_MINUS)
            rib_asm = asm.make_sub(rib_plane_bx, AxDir3.Y_PLUS)
            rib_elem = ExtrudedBlock(
                TrapezoidFigure(rib_size.x, rib_size.z, 30), rib_size.y
            )
            rib_asm.place_block(rib_elem)

        add_rib(Dir2.Y_PLUS)
        add_rib(Dir2.Y_MINUS)

    # features
    if features is not None:
        style.layout.render_features(features, asm, feature_area)

    return asm.make_rendering()
