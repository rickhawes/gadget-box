"""Rendering of a 3D printable model."""

from dataclasses import dataclass
from typing import Sequence

import build123d as bd
import ocp_vscode as viewer

from .geometry import Mm


@dataclass(frozen=True)
class Rendering:
    """The the output of a render function that can be shown or exported.

    See Also:
        `render_rack_faceplate` - Example model rendering function
        `show_multiple` - If multiple renderings need to be shown together.
    """

    part: bd.Part | bd.Compound
    label: str | None

    def show(self) -> None:
        """Show the rendering in the OCP Viewer."""
        viewer.show(self.part)

    def export_step(self, filename: str) -> None:
        """Export the rendering into a STEP file."""
        if not bd.export_step(self.part, filename):
            raise IOError("Export of STEP file failed.")

    def export_stl(self, filename: str) -> None:
        """Export the rendering into a STL file."""
        if not bd.export_stl(self.part, filename):
            raise IOError("Export of a STL file failed.")


def show_multiple(
    renderings: Sequence[Rendering], spacing: Mm = 10, max_per_row: int = 4
) -> None:
    """Show multiple renderings in a grid fashion.

    Args:
        renderings: The renderings to show
        max_per_row: The number of rendering in a row
    """
    bounding_boxes = [r.part.bounding_box() for r in renderings]
    x = 0
    y = 0
    moved_parts: list[bd.Part | bd.Compound] = []
    for i, rendering in enumerate(renderings):
        moved_part = bd.Location((x, y)) * rendering.part
        moved_parts.append(moved_part)
        if i % max_per_row != max_per_row - 1:
            x += bounding_boxes[i].size.X + spacing
        else:
            x = 0
            y += max(b.size.Y for b in bounding_boxes[i - (max_per_row - 1) : i])
    viewer.show(moved_parts)
