"""This example demonstrates a faceplate with a puck holder."""

from gadget_box import PuckHolder, Vec3, render_rack_faceplate

holder = PuckHolder(
    device_size=Vec3(60, 30, 60),
    device_rounding=10,
    style=PuckHolder.Style(has_cutout=True),
)
plate = render_rack_faceplate(rack_units=1.0, features=[[holder]])

# Show the plate in the OCP viewer
plate.show()

# Export the plate as a STEP file as well
plate.export_step("outputs/face_plate_with_puck.step")
