"""Test blocks."""

import gadget_box as gb

BLK = "Block Tests"


def test_counter_sink(viewer_logger: gb.TestLogger) -> None:
    blk = gb.CounterSinkBlock(hole_diameter=3, top_diameter=6, length=8, top_length=1)
    viewer_logger.log(blk.render().part, BLK)
