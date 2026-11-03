from mini_rack_printables import Keystone, XRayShow, feature_xray

#
# This example demonstrates a keystone cutout.
#
plate = feature_xray(Keystone(), show=XRayShow.ALL)

# Show the plate in the OCP viewer
plate.show()
