"""This example demonstrates a faceplate with a Jet KVM cutout."""

from gadget_box import JetKVM, render_rack_faceplate

plate = render_rack_faceplate(rack_units=1.5, features=[[JetKVM()]])

# Show the plate in the OCP viewer
plate.show()

# Export the plate as a STEP file as well
plate.export_step("outputs/face_plate_with_jetkvm.step")
