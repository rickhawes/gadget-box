from mini_rack_printables import (
    CircleFigure,
    Cutout,
    Dir2,
    FaceplateStyle,
    RectangleFigure,
    RowLayout,
    SlotFigure,
    faceplate,
)
from mini_rack_printables.models.faceplate import FaceplateStyle

#
# This example demonstrates a faceplate with a RowLayout containing 3 cutouts.
# Each cutout has a different alignment and padding and shift amount.
#

# Cutout
partLeft = Cutout(CircleFigure(5.0))
partCenter = Cutout(RectangleFigure(10.0, 5.0))
partRight = Cutout(SlotFigure(10.0, 5.0), rib=FaceplateStyle.STD_RIB)

# A basic faceplate with row layout
plate = faceplate(
    rack_units=1.0,
    features=[[partLeft, partCenter, partRight]],
    layout=RowLayout(place=Dir2.SIDE_BOTTOM),
)

# Show the plate in the OCP viewer
plate.show()

# Export the plate as a STEP file as well
plate.export_step("outputs/face_plate_with_div.step")
