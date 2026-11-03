from mini_rack_printables import CornerHolder, RectangleFigure, feature_xray

#
# This example demonstrates a corner holder part.
#
holder = CornerHolder(RectangleFigure(100, 100, 5), corner_width=12, corner_height=12)
plate = feature_xray(holder)

# Show the plate in the OCP viewer
plate.show()
