"""Rendering of a 3D printable model.

See Also:
    `faceplate` - Example model
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import ocp_vscode as viewer
from build123d import Compound, Part, export_step


@dataclass(frozen=True)
class Rendering:
    """The rendering of a model function and the operations that can be performed."""

    part: Part | Compound

    def show(self) -> None:
        """Show the rendering in the OCP Viewer."""
        viewer.show(self.part)

    def export_step(self, filename: str) -> None:
        """Export the rendering into a STEP file."""
        if not export_step(self.part, filename):
            raise IOError("File not saved")
