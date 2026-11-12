# pylint: disable=missing-module-docstring, duplicate-code
# <AUTOGEN_INIT>
from gadget_garb.core.assembler import (
    Assembler,
)
from gadget_garb.core.block import (
    Block,
    BoxBlock,
    ConeBlock,
    CylinderBlock,
    ExtrudedBlock,
    ImportBlock,
    PlateBlock,
    StackBlock,
    TubeBlock,
)
from gadget_garb.core.corners import (
    BeveledCorners,
    Corners,
    InsetCorners,
    RoundedCorners,
    SelectedCorners,
    SquareCorners,
)
from gadget_garb.core.feature import (
    Feature,
    FeatureList,
    Rib,
)
from gadget_garb.core.figures import (
    AlignedFigure,
    CircleFigure,
    CombinedFigure,
    CutoutFigure,
    Figure,
    Op2,
    OutsetFigure,
    RectangleFigure,
    RingFigure,
    RotatedFigure,
    SlotFigure,
    TrapezoidFigure,
    TriangleFigure,
)
from gadget_garb.core.geometry import (
    Ax2,
    Ax3,
    AxDir,
    AxDir2,
    AxDir3,
    Bx,
    Degree,
    Dir2,
    Dir3,
    Mm,
    Rc,
    Vec2,
    Vec3,
)
from gadget_garb.core.hole_patterns import (
    CircleFill,
    HexFill,
    HolePattern,
    SquareFill,
    fill_holes,
)
from gadget_garb.core.layouts import (
    GridLayout,
    Layout,
    MeasuredRowsColumns,
    RowLayout,
)
from gadget_garb.core.piece import (
    Piece,
)
from gadget_garb.core.print_dims import (
    MIN_SPAN_WIDTH,
    E,
)
from gadget_garb.core.rendering import (
    Rendering,
)
from gadget_garb.core.row_column_collection import (
    RowColumnCollection,
)
from gadget_garb.core.test_fixtures import (
    STD_PLATE_SIZE,
    TestLogger,
    XRayShow,
    feature_xray,
)

__all__ = [
    "AlignedFigure",
    "Assembler",
    "Ax2",
    "Ax3",
    "AxDir",
    "AxDir2",
    "AxDir3",
    "BeveledCorners",
    "Block",
    "BoxBlock",
    "Bx",
    "CircleFigure",
    "CircleFill",
    "CombinedFigure",
    "ConeBlock",
    "Corners",
    "CutoutFigure",
    "CylinderBlock",
    "Degree",
    "Dir2",
    "Dir3",
    "E",
    "ExtrudedBlock",
    "Feature",
    "FeatureList",
    "Figure",
    "GridLayout",
    "HexFill",
    "HolePattern",
    "ImportBlock",
    "InsetCorners",
    "Layout",
    "MIN_SPAN_WIDTH",
    "MeasuredRowsColumns",
    "Mm",
    "Op2",
    "OutsetFigure",
    "Piece",
    "PlateBlock",
    "Rc",
    "RectangleFigure",
    "Rendering",
    "Rib",
    "RingFigure",
    "RotatedFigure",
    "RoundedCorners",
    "RowColumnCollection",
    "RowLayout",
    "STD_PLATE_SIZE",
    "SelectedCorners",
    "SlotFigure",
    "SquareCorners",
    "SquareFill",
    "StackBlock",
    "TestLogger",
    "TrapezoidFigure",
    "TriangleFigure",
    "TubeBlock",
    "Vec2",
    "Vec3",
    "XRayShow",
    "feature_xray",
    "fill_holes",
]
# </AUTOGEN_INIT>
