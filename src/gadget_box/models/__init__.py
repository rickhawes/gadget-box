# pylint: disable=missing-module-docstring, duplicate-code
# <AUTOGEN_INIT>
from gadget_box.models.device_box import (
    DeviceBoxStyle,
    render_device_box,
)
from gadget_box.models.fastners import (
    LidFastener,
    MagnetLidFastner,
    MagnetLidFastners,
    NoLidFastener,
    ScrewLidFastner,
    ScrewLidFastners,
)
from gadget_box.models.rack_dims import (
    RackDims,
    RackScrewDims,
    Screw1032Dims,
    ShelfTabDims,
    rack_units_to_mm,
)
from gadget_box.models.rack_faceplate import (
    FaceplateStyle,
    render_rack_faceplate,
)
from gadget_box.models.rack_holes import (
    RackHoleFigure,
    RackHolePattern,
    layout_rack_screw_holes,
)
from gadget_box.models.rack_shelf import (
    ShelfStyle,
    render_rack_shelf,
)

__all__ = [
    "DeviceBoxStyle",
    "FaceplateStyle",
    "LidFastener",
    "MagnetLidFastner",
    "MagnetLidFastners",
    "NoLidFastener",
    "RackDims",
    "RackHoleFigure",
    "RackHolePattern",
    "RackScrewDims",
    "Screw1032Dims",
    "ScrewLidFastner",
    "ScrewLidFastners",
    "ShelfStyle",
    "ShelfTabDims",
    "layout_rack_screw_holes",
    "rack_units_to_mm",
    "render_device_box",
    "render_rack_faceplate",
    "render_rack_shelf",
]
# </AUTOGEN_INIT>
