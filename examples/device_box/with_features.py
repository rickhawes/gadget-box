"""Show a device box with multiple features and screw fasteners."""

from gadget_box.core import hole_patterns
import gadget_box as gb

# A device box has an interior size, a style and a set of back_features
size = gb.Vec3(140, 100, 31)

style = gb.DeviceBoxStyle(fastener=gb.ScrewLidFastners.M3X5_7)

features: dict[gb.AxDir3, gb.FeatureList] = {
    gb.AxDir3.TOP: [[gb.XSpacer(), gb.CornerHolder(93.24, 93.24, 16)]],
    gb.AxDir3.BOTTOM: [[gb.XSpacer(), gb.CornerHolder(93.24, 93.24, 16)]],
    gb.AxDir3.BACK: [[gb.CircleCutout(10)]],
    gb.AxDir3.RIGHT: [[gb.Spacer(more_x=True, hole_pattern=gb.HexFill())]],
    gb.AxDir3.LEFT: [[gb.Spacer(more_x=True, hole_pattern=gb.HexFill())]],
}
box, lid = gb.render_device_box(size, features, style)
gb.show_multiple([box, lid])

box.export_step("outputs/device_box_features.step")
lid.export_step("outputs/device_box_features_lid.step")
