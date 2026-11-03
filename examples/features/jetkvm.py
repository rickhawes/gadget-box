from mini_rack_printables import JetKVM, XRayShow, feature_xray

#
# This example demonstrates a Jet KVM cutout.
#
plate = feature_xray(JetKVM(), show=XRayShow.ONLY_ADDS)

# Show the plate in the OCP viewer
plate.show()
