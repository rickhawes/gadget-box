"""
Common test fixtures defined in core to be in the import path for tests.
"""

import sys
from typing import final

from build123d import Color, Compound, Part, Sketch, Solid

from .assembler import Assembler
from .feature import Feature
from .geometry import AxDir3, Bx, Vec3
from .rendering import Rendering


@final
class TestLogger:
    """Class to log a 3d printable models so they can be displayed with viewer.

    This logger is useful in testing. Defined in the core to allow to be included in tests.


    """

    type LogableType = Part | Compound | Sketch

    @final
    class LogEntry:
        def __init__(
            self, group_name: str, function_name: str, part: TestLogger.LogableType
        ) -> None:
            self.group_name = group_name
            self.function_name = function_name
            self.part = part
            self.size = part.bounding_box().size

    entries: dict[str, list[LogEntry]] = {}

    def log(self, part: TestLogger.LogableType | Rendering, group: str | None = None) -> None:
        frame = sys._getframe(1)
        assert frame is not None
        group_name = group if group is not None else frame.f_globals["__name__"]
        function_name = frame.f_code.co_name
        if isinstance(part, Rendering):
            part = part.part
        entry = TestLogger.LogEntry(group_name, function_name, part)
        if group_name not in self.entries:
            self.entries[group_name] = []
        self.entries[group_name].append(entry)


STD_PLATE_SIZE = Vec3(100, 100, 5)


def feature_xray(
    feature: Feature,
    plate_size: Vec3 = STD_PLATE_SIZE,
    only_adds: bool = False,
    only_cuts: bool = False,
) -> Rendering:
    """Render the feature with an invisible plate.

    Adds are colored blue and subtracts are colored .

    Args:
        feature (Feature): The feature to render.
        plate_size (Vec3): The plate_size to pass to the feature's render method.
        only_adds: Only show the adds from the feature.
        only_cuts: Only show the cuts from the feature.
    """

    plate = Bx(plate_size, Vec3(0, 0, plate_size.z / 2))
    asm = Assembler(plate, z_dir=AxDir3.TOP)

    feature.render(asm)
    children: list[Part | Solid] = []
    for piece in asm.all_pieces():
        if not piece.cut:
            if not only_cuts:
                new_piece = piece.set(color=Color("blue"), label="add")
                children.append(new_piece.part)
        else:
            if not only_adds:
                new_piece = piece.set(color=Color("red"), label="subtract")
                children.append(new_piece.part)

    return Rendering(Compound(label="xray", children=children))
