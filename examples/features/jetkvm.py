"""This example demonstrates a Jet KVM cutout."""

from gadget_garb import JetKVM, XRayShow, feature_xray

model = feature_xray(JetKVM(), show=XRayShow.ONLY_ADDS)
# Show the model in the OCP viewer
model.show()
