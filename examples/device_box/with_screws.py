"""Show a basic device box with screw fasteners."""

import gadget_box as gb

style = gb.DeviceBoxStyle(fastener=gb.ScrewLidFastners.M3X5_7)
features = [[gb.CornerHolder(93.24, 93.24, 16)]]
box, lid = gb.render_device_box(
    gb.Vec3(100, 100, 31), 
    {gb.AxDir3.TOP: features, gb.AxDir3.BOTTOM: features},
    style=style
)
gb.show_multiple([box, lid])

box.export_step("outputs/device_box_screws.step")
lid.export_step("outputs/device_box_screws_lid.step")
