"""This example demonstrates a basic shelf with default settings."""

from gadget_garb import rack_shelf

shelf = rack_shelf(rack_units=1.0)

# Show the shelf in the viewer. Run 'task viewer' before.
shelf.show()

# Export the shelf to a STEP file
shelf.export_step("outputs/basic_shelf.step")
