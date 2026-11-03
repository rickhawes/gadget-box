from mini_rack_printables import Keystone, feature_xray

#
# This example demonstrates a keystone cutout.
#
plate = feature_xray(Keystone(), only_adds=False)

# Show the plate in the OCP viewer
plate.show()
