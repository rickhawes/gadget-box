"""This example demonstrates a faceplate with a holder."""

from gadget_garb import BoxHolder, Vec3, rack_faceplate

holder = BoxHolder(device_size=Vec3(210.0, 33.1, 30), style=BoxHolder.BACK_LIP)
plate = rack_faceplate(rack_units=1.0, features=[[holder]])

# Show the plate in the OCP viewer
plate.show()

# Export the plate as a STEP file as well
plate.export_step("outputs/face_plate_with_holder.step")
