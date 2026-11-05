from dataclasses import dataclass
from typing import Sequence, final

from build123d import BuildPart, Location, Mode, Plane, insert

from .block import Block
from .geometry import AxDir3, Bx, Dir2, Mm, Rc, Vec2, Vec3
from .piece import Piece
from .rendering import Rendering


@final
class Assembler:
    """Helper to assemble blocks for models and features.

    See Also:
        `Model` - Used by Model subclasses to assemble blocks together
        `Feature` - Used by Feature subclasses to assemble blocks together
        `Block` - the building blocks that are assembled together
    """

    # the base to place things on
    base: Bx
    """the base plate (global coordinates)"""
    plate_side: AxDir3
    """The side of the base to place other objects"""
    cutout_mode: bool
    """The default for the cut parameter for pieces rendered by blocks"""

    # the orientation of the plane
    z_dir: AxDir3
    """The direction of the Assembler's plane"""
    _plane: Plane
    """The plane of the model to place blocks (global coordinates)"""

    # Output
    parent: Assembler | None = None
    """If this is a sub-assembler, then the parent assembler."""
    sub_assemblers: list[Assembler]
    """Assemblers attached to this model"""
    _pieces: list[Piece] | None = None
    """If this is a top-level assembler, all the pieces"""
    bounds: Bx | None = None
    """The bounds of all pieces"""

    # properties
    @property
    def plate_bx(self) -> Bx:
        """The base bx (Assembler coordinates)"""
        rc = self.plate_rc
        d = self.plate_depth
        z = d / 2 if self.cutout_mode else -d / 2
        return Bx((rc.size.x, rc.size.y, d), (0, 0, z))

    @property
    def plate_rc(self) -> Rc:
        """The base rc (Assembler coordinates)"""
        return Rc(self.base.side_rc(self.plate_side).size)

    @property
    def plate_depth(self) -> Mm:
        """The base depth (Assembler coordinates)"""
        return self.base.side_depth(self.plate_side)

    @property
    def origin(self) -> Vec3:
        """The assembler's origin in the global coordinates"""
        return self.base.side_bx(self.plate_side).center

    def __init__(
        self,
        plate: Bx,
        z_dir: AxDir3 = AxDir3.Z_PLUS,
        cutout_mode: bool = False,
        parent: Assembler | None = None,
    ) -> None:
        """Create an assembler or sub-assembler.

        Args:
            plate: the base box on which everything is placed in global.
            z_dir: the orientation for the placement (and the z_dir).
            cutout_mode: the default cut value for block placement and the base is above the plane.
            parent: the parent assembler if any.
        """
        self.base = plate
        self.z_dir = z_dir
        self.plate_side = z_dir.to_opposite() if cutout_mode else z_dir
        self.cutout_mode = cutout_mode

        # make internal structures
        self._plane = Plane(
            origin=plate.side_bx(self.plate_side).center.to_vector(),
            z_dir=z_dir.to_plane_z_dir(),
            x_dir=z_dir.to_plane_x_dir(),
        )

        # accumulations
        self._pieces = []
        self.sub_assemblers = []
        self.parent = parent
        self.bounds = None

    # region Create assemblers and sub-assemblers

    @classmethod
    def make(
        cls,
        base: Bx,
        z_dir: AxDir3 = AxDir3.Z_PLUS,
        cutout_mode: bool = False,
    ) -> Assembler:
        """Create a top-level assembler.

        Args:
            plate: the base box on which everything is placed in global.
            z_dir: the orientation for the placement (and the z_dir).
            cutout_mode: the default cut value for block placement and the base is above the plane.
        """
        return Assembler(base, z_dir, cutout_mode, parent=None)

    @classmethod
    def make_with_block(
        cls, block: Block, center: Vec3 | None = None, z_dir: AxDir3 = AxDir3.Z_PLUS
    ) -> Assembler:
        """Create top-level assembler with the block as the plate.

        Args:
            block (Block) - the base object relative to the XY plane
            center (Vec3) - relative to the XY plane
            z_dir (AxDir3) - the side of the base to form the assembler
        """
        if center is None:
            center = Vec3(0, 0, block.size.z / 2)
        bx = Bx(block.size, center)
        asm = Assembler.make(bx, z_dir)
        piece = block.render(cut=False).moved(center)
        asm._append_piece(piece)
        return asm

    def make_sub(
        self,
        plate: Bx | None = None,
        z_dir: AxDir3 | None = None,
        cutout_mode: bool | None = None,
    ) -> Assembler:
        """Create a sub-assembler with defaults of the current assembler.

        Args:
            plate (Bx) - plate in relative to self
            z_dir (AxDir3) - the sub's z_dir and side of plate to use
            cutout_mode (bool) - The assembler should default to cutting from the plate
        """
        if plate is None:
            # take the current plate which is global and make a local copy
            center = self.base.center - self.origin
            plate = Bx(self.base.size, center)
        global_plate = plate.move(self.origin)
        if z_dir is None:
            z_dir = self.z_dir
        if cutout_mode is None:
            cutout_mode = self.cutout_mode
        assembler = Assembler(global_plate, z_dir, cutout_mode, parent=self)
        self.sub_assemblers.append(assembler)
        return assembler

    def make_cutout_sub(self) -> Assembler:
        if self.cutout_mode:
            raise RuntimeError("Cannot make a cutout sub on a cutout sub")
        return self.make_sub(cutout_mode=True)

    def make_section_sub(self, section: Rc, origin: Vec2) -> Assembler:
        """Section relative to the plane_rc"""
        size = Vec3(section.size.x, section.size.y, self.plate_depth)
        center = Vec3(origin.x, origin.y, self.plate_bx.center.z)
        return self.make_sub(Bx(size, center))

    # #endregion

    @dataclass(frozen=True)
    class Place:
        """Specifies a location relative to the base plane and bounds."""

        origin: Dir2 = Dir2.CENTER
        """The region of the base where the origin is. The origin takes into account the size of the object being placed."""
        offset: Vec2 | Vec3 = Vec2(0, 0)
        """The offset of the center."""

    type Places = Assembler.Place | Sequence[Assembler.Place]

    def place_bounds(self, size: Vec3, place: Place = Place()) -> Bx:
        """The bounding box of `size` relative the assembler's plane"""
        origin = self.plate_rc.place_center(Rc(size.x, size.y), place.origin).to_vec3()
        offset = (
            place.offset if isinstance(place.offset, Vec3) else place.offset.to_vec3()
        )
        center = origin + offset + Vec3(0, 0, size.z / 2)
        return Bx(size, center)

    def place_block(
        self, block: Block, places: Places = Place(), cut: bool | None = None
    ) -> None:
        """Place an block"""
        if isinstance(places, Assembler.Place):
            places = [places]
        if len(places) == 0:
            raise ValueError("`place` must not be an empty list")
        resolved_cut = cut if cut is not None else self.cutout_mode
        for p in places:
            center = self.place_bounds(block.size, p).center
            piece = block.render(resolved_cut)
            self.add_piece(piece, center)

    def stack_block(
        self, block: Block, place: Place = Place(), sub_z_dir: AxDir3 = AxDir3.Z_PLUS
    ) -> Assembler:
        """Place an block and create a sub-assembler on the placed."""
        center = self.place_bounds(block.size, place).center
        piece = block.render(cut=False)
        self.add_piece(piece, center)
        return self.make_sub(Bx(block.size, center), z_dir=sub_z_dir)

    def add_piece(self, piece: Piece, position: Vec3 = Vec3(0, 0, 0)) -> None:
        """Add pieces to the model at `position` relative to the assembler's plane."""
        moved_piece = piece.moved(self._plane * Location(position.to_vector()))
        self._append_piece(moved_piece)

    def _append_piece(self, piece: Piece) -> None:
        """Append `piece` to the top-level assembler's list"""
        # Update bounds
        if not piece.cut:
            relative = piece.bounds.move(-self.origin)
            if self.bounds is None:
                self.bounds = relative
            else:
                self.bounds = Bx.union(self.bounds, relative)
        # Place in the top-level list
        if self.parent is None:
            assert self._pieces is not None
            self._pieces.append(piece)
        else:
            self.parent._append_piece(piece)

    def to_global(self, local: Vec3) -> Vec3:
        return local + self.origin

    def to_local(self, gbl: Vec3) -> Vec3:
        return gbl - self.origin

    # def _get_plane(self) -> Plane | Location:
    #     if self.parent is None:
    #         return self._plane
    #     else:
    #         return self.parent._get_plane() * self._plane

    def all_pieces(self) -> list[Piece]:
        """All the pieces in the top and sub assemblers."""
        if self._pieces is None:
            assert self.parent is not None
            return self.parent.all_pieces()
        else:
            return self._pieces

    def make_rendering(self) -> Rendering:
        with BuildPart() as builder:
            for p in self.all_pieces():
                mode = Mode.SUBTRACT if p.cut else Mode.ADD
                _ = insert(p.part, mode=mode)
        assert builder.part is not None
        return Rendering(builder.part)
