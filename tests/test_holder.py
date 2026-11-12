from gadget_garb import (
    BoxHolder,
    GeneralCornerHolder,
    PuckHolder,
    RectangleFigure,
    TestLogger,
    Vec3,
    feature_xray,
)


def test_default_holder(viewer_logger: TestLogger) -> None:
    holder = BoxHolder(device_size=Vec3(30, 20, 20))
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)


def test_no_rounding(viewer_logger: TestLogger) -> None:
    holder = BoxHolder(device_size=Vec3(30, 20, 20), device_rounding=0.0)
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)


def test_back_lip(viewer_logger: TestLogger) -> None:
    holder = BoxHolder(device_size=Vec3(30, 20, 20), style=BoxHolder.BACK_LIP)
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)


def test_no_cutout(viewer_logger: TestLogger) -> None:
    holder = BoxHolder(device_size=Vec3(30, 20, 20), style=BoxHolder.NO_CUTOUT)
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)


def test_puck_holder(viewer_logger: TestLogger) -> None:
    holder = PuckHolder(device_size=Vec3(80, 20, 80), device_rounding=10)
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)


def test_corner_holder(viewer_logger: TestLogger) -> None:
    holder = GeneralCornerHolder(RectangleFigure(80, 30, 2))
    rendering = feature_xray(holder)
    viewer_logger.log(rendering)
