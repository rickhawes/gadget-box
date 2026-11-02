from functools import cached_property
from importlib.resources import as_file, files
from pathlib import Path
from typing import override

from ..core.assembler import Assembler
from ..core.elements_3d import BoxElement, ImportElement
from ..core.feature import Feature
from ..core.geometry import Bx
from ..core.piece import Piece


class ImportFeature(Feature):
    """A Feature formed using a STL or BREP file"""

    ASSET_PATH: str = "mini_rack_printables.assets"

    cutout: bool = True
    element: ImportElement

    def __init__(
        self,
        file: str | None = None,
        asset: str | None = None,
        cutout: bool = True,
    ) -> None:
        """
        Initialize the ImportPart with the given path or asset name and optional parameters.

        Args:
            file (Path): The path to the BREP or STL file.
            asset (str): The name of the asset to import.
            cutout (bool, optional): Whether to cut out the part from the enclosing model or place on top of it. Defaults to True.
        """
        self.cutout = cutout
        if file is not None:
            self.element = ImportElement(file=Path(file))
        elif asset is not None:
            self.element = ImportElement(asset=Path(ImportFeature.ASSET_PATH + "/" + asset))
        else:
            raise ValueError("Either path or asset must be provided")

    @override
    def desired_size(self) -> Feature.DesiredSize:
        return Feature.DesiredSize(self.element.size.to_2d(), False)

    @override
    def render(self, asm: Assembler) -> None:
        if self.cutout:
            # Cutout the plate first
            cutout_asm = asm.make_cutout_sub()
            box = BoxElement(dx=self.element.size.x, dy=self.element.size.y, dz=asm.plate_depth)
            cutout_asm.place_element(box)
            # Add the import element in the cutout (explicitly override the cut mode)
            cutout_asm.place_element(self.element, cut=False)
        else:
            # Add the imported block on the plate
            asm.place_element(self.element)
