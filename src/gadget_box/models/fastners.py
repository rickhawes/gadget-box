"""Classes for rendering for common fasterner."""

from dataclasses import dataclass
from enum import Enum
from typing import override

from gadget_box.core import Assembler, AxDir3, CounterSinkBlock, CylinderBlock, Mm, Vec3


@dataclass(frozen=True)
class LidFastener:
    """Abstract class that defines a pair of fasteners for a base and lid.

    Note this doesn't use the ABC class because the ABC meta class doesn't mix with
    an Enum meta class.
    """

    @property
    def layout_radius(self) -> Mm:
        """Amount of space that this fastener will take in layout.

        Layout space include space for holes and for needed walls around the holes.
        Should be considered a minimum.
        """
        raise NotImplementedError()

    def render_lid(self, asm: Assembler, places: Assembler.Places) -> None:
        """Render the lid hole.

        Lids are assembled to be printed, which has the top of the lid as the bottom
        of the print. The assembler's plate is the lid.
        """
        raise NotImplementedError()

    def render_base(self, asm: Assembler, places: Assembler.Places) -> None:
        """Render the base hole.

        Base are assembled to be printed, which means that assembler's plate is

        """
        raise NotADirectoryError()


@dataclass(frozen=True)
class NoLidFastener(LidFastener):
    """No lid"""

    @override
    @property
    def layout_radius(self) -> Mm:
        return 0

    @override
    def render_lid(self, asm: Assembler, places: Assembler.Places) -> None:
        pass

    @override
    def render_base(self, asm: Assembler, places: Assembler.Places) -> None:
        pass


@dataclass(frozen=True)
class ScrewLidFastner(LidFastener):
    """The lid has a countersunk flat screw and bottom has screw insert"""

    lid: CounterSinkBlock
    base: CylinderBlock
    radius: Mm

    @override
    @property
    def layout_radius(self) -> Mm:
        return self.radius

    @override
    def render_lid(self, asm: Assembler, places: Assembler.Places) -> None:
        bottom_size = asm.plate_rc.size.to_vec3(0)
        bottom_offset = Assembler.Place(offset=Vec3(0, 0, -asm.plate_depth))
        bottom_bx = asm.place_bx(bottom_size, bottom_offset)
        bottom_asm = asm.make_sub(bottom_bx, z_dir=AxDir3.Z_MINUS)
        bottom_asm.place_block(self.lid, places, cut=True)

    @override
    def render_base(self, asm: Assembler, places: Assembler.Places) -> None:
        asm.place_block(self.base, places, cut=True)


class ScrewLidFastners(ScrewLidFastner, Enum):
    """A set of common LidFastener"""

    # see https:https://www.prusa3d.com/content/wysiwyg/fotky/cnc-k/sizes_chart.png
    # for a list of standard heat-set threaded inserts and their hole dimensions
    #
    # see https://engineersbible.com/countersunk-machine-ansi-metric/
    # for a list of standard countersunk metric screw hole dimensions
    M3X5_7 = (
        CounterSinkBlock(
            hole_diameter=3.2, length=8, top_diameter=6.2, top_length=0.6
        ),  # M3 Screw
        CylinderBlock(radius=2.0, height=6.7),  # M3x5.7 heat-set insert
        5,  # M3 insert min rounded to the nearest
    )


@dataclass(frozen=True)
class MagnetLidFastner(LidFastener):
    """The lid fastner uses two magnets."""

    diameter: Mm
    depth: Mm
    gap: Mm = 0.1
    thickness: Mm = 1.9

    @override
    @property
    def layout_radius(self) -> Mm:
        return self.diameter / 2 + self.gap + self.thickness

    @override
    def render_lid(self, asm: Assembler, places: Assembler.Places) -> None:
        hole = CylinderBlock(self.diameter / 2 + self.gap, self.depth)
        asm.place_block(hole, places, cut=True)

    @override
    def render_base(self, asm: Assembler, places: Assembler.Places) -> None:
        hole = CylinderBlock(self.diameter / 2 + self.gap, self.depth)
        asm.place_block(hole, places, cut=True)


class MagnetLidFastners(MagnetLidFastner, Enum):
    """A set of fasteners using common lid sizes"""

    # see https://www.apexmagnets.com/magnets/metric-sizes
    # for a list of standard magnetic size.
    M4X2 = (4, 2)
    M6X2 = (6, 2)
    M6X3 = (6, 3)
