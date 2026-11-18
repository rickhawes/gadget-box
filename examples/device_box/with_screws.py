"""Show a basic device box with screw fasteners."""

import gadget_box as gb

style = gb.DeviceBoxStyle(fastener=gb.ScrewLidFastners.M3X5_7)
box, lid = gb.render_device_box(gb.Vec3(100, 100, 31), style=style)
gb.show_multiple([box, lid])
