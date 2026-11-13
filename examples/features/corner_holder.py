"""Shows a corner holder feature."""

from gadget_box import CircleFigure, GeneralCornerHolder, Vec2, feature_xray

holder = GeneralCornerHolder(CircleFigure(50), opening=Vec2(10, 10))
model = feature_xray(holder)

# Show the model in the OCP viewer
model.show()
