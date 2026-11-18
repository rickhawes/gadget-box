"""A basic device enclosure."""

from dataclasses import dataclass
from typing import Sequence

from gadget_box.core import (
    Assembler,
    Ax3,
    AxDir3,
    Bx,
    CutoutFigure,
    ExtrudedBlock,
    FeatureList,
    Figure,
    GridLayout,
    Layout,
    Mm,
    Rc,
    RectangleFigure,
    Rendering,
    RoundedInsetCorners,
    TubeBlock,
    Vec2,
    Vec3,
)
from gadget_box.models.fastners import NoLidFastener

from .fastners import LidFastener, NoLidFastener


@dataclass(frozen=True)
class DeviceBoxStyle:
    """The set of parameters for the box."""

    @dataclass(frozen=True)
    class Base:
        """Base style"""

        thickness: Mm = 4.0
        """the base of the box"""
        layout: Layout = GridLayout()
        """the layout of the base of the grid"""

    @dataclass(frozen=True)
    class Wall:
        """Wall style parameters."""

        thickness: Mm = 4.0
        """The thickness of the wall. Divided for the lip."""
        layout: Layout = GridLayout()
        """Feature layout"""

    @dataclass(frozen=True)
    class Lid:
        """Lid style"""

        thickness: Mm = 4.0
        """Thickness of the lid"""
        lip_depth: Mm = 2.0
        """Depth of the lip of the lid."""
        lip_gap: Mm = 0.1
        """Gap in the lip of the lid."""
        layout: Layout = GridLayout()
        """Feature layout"""

    base: Base = Base()
    """Base parameters."""
    wall: Wall = Wall()
    """Wall and corner parameters"""
    lid: Lid = Lid()
    """Lid and lip parameters."""
    fastener: LidFastener = NoLidFastener()
    """Magnet parameters for lid and corners."""


def render_device_box(
    interior_size: Vec3,
    features_by_side: dict[AxDir3, FeatureList] | None = None,
    style: DeviceBoxStyle = DeviceBoxStyle(),
) -> tuple[Rendering, Rendering]:
    """Assemble a basic device box with a base and a lid.

    The walls and corner posts increase the exterior volume of the box.

    Args:
        interior_size (Vec3): The interior volume excluding the walls and corner insets
        features_by_side: The feature list for side.
        style (DeviceBoxStyle): All the information about box
    """
    if features_by_side is None:
        features_by_side = {}

    inner_outline, lip_outline, outer_outline = _common_figures(interior_size, style)

    def assemble_box() -> Assembler:
        """Create an assembler with the lid"""
        # start with the base plate
        base_asm = Assembler.make_with_block(
            ExtrudedBlock(outer_outline, style.base.thickness)
        )
        # add base features
        if AxDir3.BOTTOM in features_by_side:
            features = features_by_side[AxDir3.BOTTOM]
            style.base.layout.render_features(
                features, base_asm, Rc(interior_size.to_2d())
            )

        # add walls
        wall_base_block = ExtrudedBlock(
            CutoutFigure(outer_outline, inner_outline),
            interior_size.z - style.Lid.lip_depth,
        )
        lip_asm = base_asm.stack_block(wall_base_block)
        # add lip
        wall_lip_block = ExtrudedBlock(
            CutoutFigure(lip_outline, inner_outline), style.Lid.lip_depth
        )
        top_asm = lip_asm.stack_block(wall_lip_block)
        # add fasteners
        style.fastener.render_base(top_asm, _fastener_places(interior_size, style))

        # add wall features or holes
        cx = cy = style.fastener.layout_radius * 2
        dz = interior_size.z
        base_size = base_asm.plate_bx.size
        walls_bx = Bx(base_size.x, base_size.y, dz, 0, 0, dz / 2)
        for wall_dir in [AxDir3.LEFT, AxDir3.RIGHT, AxDir3.FRONT, AxDir3.BACK]:
            if wall_dir in features_by_side:
                wall_bx = walls_bx.side_bx(wall_dir, depth=style.wall.thickness)
                inset_wall_bx = _resize_bx_along_axis(
                    wall_bx,
                    Vec3(-2 * cx, -2 * cy, -2 * style.lid.lip_depth),
                    wall_dir.to_ax3(),
                )
                wall_asm = base_asm.make_sub(inset_wall_bx, wall_dir.to_opposite())
                features = features_by_side[wall_dir]
                style.wall.layout.render_features(features, wall_asm)

        return base_asm

    # lid rendered with the base on the bottom
    def assemble_lid() -> Assembler:
        """Create an assembler with the lid."""
        base_block = ExtrudedBlock(outer_outline, style.lid.thickness)
        lip_block = TubeBlock(
            outer_outline,
            -(style.wall.thickness / 2 - style.lid.lip_gap),  # sub the lip gap
            style.lid.lip_depth,
        )
        asm = Assembler.make_with_block(base_block)
        style.fastener.render_lid(asm, _fastener_places(interior_size, style))
        asm.place_block(lip_block)
        # add features if present
        if AxDir3.TOP in features_by_side:
            features = features_by_side[AxDir3.TOP]
            style.lid.layout.render_features(features, asm, Rc(interior_size.to_2d()))
        return asm

    box_asm = assemble_box()
    lid_asm = assemble_lid()
    return box_asm.render(label="box"), lid_asm.render(label="lid")


def _common_figures(size: Vec3, style: DeviceBoxStyle) -> tuple[Figure, Figure, Figure]:
    """Create the inner, lip, and outer outline figures."""
    wt = style.wall.thickness
    wtv = Vec2(wt, wt)
    cx = cy = style.fastener.layout_radius * 2

    inner_r = style.fastener.layout_radius
    inner_size = size.to_2d() + 2 * Vec2(cx, cy)
    lip_r = inner_r + 0.5 * wt
    lip_size = inner_size + wtv
    outer_r = lip_r + 0.5 * wt
    outer_size = lip_size + wtv

    # common figures
    c = RoundedInsetCorners(cx, cy) if cx > 0 and cy > 0 else None
    inner_outline = RectangleFigure(inner_size.x, inner_size.y, corners=c)
    lip_outline = RectangleFigure(lip_size.x, lip_size.y, lip_r)
    outer_outline = RectangleFigure(outer_size.x, outer_size.y, outer_r)
    return inner_outline, lip_outline, outer_outline


def _fastener_places(size: Vec3, style: DeviceBoxStyle) -> Sequence[Assembler.Place]:
    """Return a list of asmemblers placed at the corners for fasteners"""
    r = style.fastener.layout_radius
    mag_rc = Rc(size.to_2d() + Vec2(2 * r, 2 * r))
    return Assembler.Place.make_at_corners(mag_rc)


def _resize_bx_along_axis(bx: Bx, amount: Vec3, axis: Ax3) -> Bx:
    """Resize the bx but not in the axis direction."""
    match axis:
        case Ax3.X:
            return Bx(bx.size + Vec3(0, amount.y, amount.z), bx.center)
        case Ax3.Y:
            return Bx(bx.size + Vec3(amount.x, 0, amount.z), bx.center)
        case Ax3.Z:
            return Bx(bx.size + Vec3(amount.x, amount.y, 0), bx.center)
