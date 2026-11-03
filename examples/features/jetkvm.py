from mini_rack_printables import JetKVM, feature_xray

#
# This example demonstrates a Jet KVM cutout.
#
plate = feature_xray(JetKVM(), only_adds=True)

# Show the plate in the OCP viewer
plate.show()
