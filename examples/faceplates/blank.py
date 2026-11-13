"""This example demonstrates a blank faceplate with a rib."""

from gadget_box import render_rack_faceplate

plate = render_rack_faceplate(rack_units=1.0)

# Show the plate in the viewer. Run 'task viewer' before.
plate.show()

# Export the plate to a STEP file
plate.export_step("outputs/blank_face_plate.step")
