"""This example shows a PuckHolder."""

from gadget_garb import PuckHolder, Vec3, feature_xray

holder = PuckHolder(
    device_size=Vec3(100, 40, 100),
    device_rounding=10,
    style=PuckHolder.Style(has_cutout=True),
)
model = feature_xray(holder)

# Show the model in the OCP viewer
model.show()
