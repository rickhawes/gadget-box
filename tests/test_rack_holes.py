# Layout tests
#
from gadget_box import (
    RackDims,
    RackScrewDims,
    Vec2,
    layout_rack_screw_holes,
    rack_units_to_mm,
)


def test_layout_rack_screw_holes_1u() -> None:
    values = layout_rack_screw_holes(rack_units=1.0)

    assert len(values) == 6
    dy = rack_units_to_mm(1.0)
    assert values[0] == Vec2(-RackScrewDims.DX / 2, RackScrewDims.BOTTOM - dy / 2)
    assert values[2] == Vec2(-RackScrewDims.DX / 2, RackScrewDims.MIDDLE - dy / 2)
    assert values[4] == Vec2(-RackScrewDims.DX / 2, RackScrewDims.TOP - dy / 2)


def test_layout_rack_screw_holes_3u() -> None:
    values = layout_rack_screw_holes(rack_units=3.0)

    assert len(values) == 18
    dy = rack_units_to_mm(3.0)
    assert values[0] == Vec2(-RackScrewDims.DX / 2, RackScrewDims.BOTTOM - dy / 2)
    assert values[2] == Vec2(-RackScrewDims.DX / 2, RackScrewDims.MIDDLE - dy / 2)
    assert values[16] == Vec2(
        -RackScrewDims.DX / 2, RackScrewDims.TOP + 2 * RackDims.HEIGHT_1U - dy / 2
    )


def test_layout_rack_screw_holes_2u_without_middle_holes() -> None:
    values = layout_rack_screw_holes(rack_units=2.0, middle_holes=False)

    assert len(values) == 8
    dy = rack_units_to_mm(2.0)
    assert values[0].y == RackScrewDims.BOTTOM - dy / 2
    assert values[2].y == RackScrewDims.TOP - dy / 2
    assert values[6].y == RackScrewDims.TOP + 1 * RackDims.HEIGHT_1U - dy / 2


def test_layout_rack_screw_holes_half_u() -> None:
    values = layout_rack_screw_holes(rack_units=0.5)

    dy = rack_units_to_mm(0.5)
    assert len(values) == 4
    assert values[0].y == RackScrewDims.BOTTOM - dy / 2
    assert values[2].y == RackScrewDims.MIDDLE - dy / 2


def test_layout_rack_screw_holes_1_5u() -> None:
    values = layout_rack_screw_holes(rack_units=1.5)

    assert len(values) == 10
    dy = rack_units_to_mm(1.5)
    assert values[0].y == RackScrewDims.BOTTOM - dy / 2
    assert values[2].y == RackScrewDims.MIDDLE - dy / 2
    assert values[8].y == RackScrewDims.MIDDLE + RackDims.HEIGHT_1U - dy / 2
