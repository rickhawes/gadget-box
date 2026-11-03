from mini_rack_printables import Keystone, faceplate

#
# This example demonstrates a faceplate with a keystone cutout.
#

# A basic horizontal layout for 3 keystones
keystone_part = Keystone()
plate = faceplate(rack_units=1.0, features=[[keystone_part for _ in range(3)]])

# Show the plate in the OCP viewer
plate.show()

# Export the plate as a STEP file as well
plate.export_step("outputs/face_plate_with_keystone.step")
