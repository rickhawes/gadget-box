from mini_rack_printables import Cutout, FaceplateStyle, SlotFigure, feature_xray

#
# This example demonstrates a corner holder part.
#
cutout = Cutout(SlotFigure(10.0, 5.0), rib=FaceplateStyle.STD_RIB)
plate = feature_xray(cutout)

# Show the plate in the OCP viewer
plate.show()
