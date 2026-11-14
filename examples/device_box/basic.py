"""Show a basic device box."""

import gadget_box as gb

box, lid = gb.render_device_box(gb.Vec3(100, 100, 30))
gb.show_multiple([box, lid])

box.export_step("outputs/device_box.step")
lid.export_step("outputs/device_box_lid.step")
