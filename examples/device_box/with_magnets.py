"""Show a basic device box."""

import gadget_box as gb

style = gb.DeviceBoxStyle(fastener=gb.MagnetLidFastners.M6X2)
box, lid = gb.render_device_box(gb.Vec3(100, 100, 30), style=style)
gb.show_multiple([box, lid])
