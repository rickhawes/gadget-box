"""A 10-inch rack shelf example with features."""

from mini_rack_printables import CornerHolder, Keystone, ShelfStyle, Spacer, shelf

shelf = shelf(
    rack_units=1.0,
    style=ShelfStyle.CLOSE_FACE,
    base_features=[[CornerHolder(100, 100, 10)]],
    face_features=[[Spacer(10, 10, more_x=True), Keystone()]],
)

# Show the shelf in the viewer. Run 'task viewer' before.
shelf.show()

# Export the shelf to a STEP file
shelf.export_step("outputs/shelf_with_features.step")
