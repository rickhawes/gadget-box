"""Minimal example of a faceplate with a circle cutout feature"""

from gadget_garb import CircleFigure, Cutout, FaceplateStyle, render_rack_faceplate

cutout = Cutout(CircleFigure(10.0), rib=FaceplateStyle.STD_RIB)
plate = render_rack_faceplate(rack_units=1.0, features=[[cutout, cutout]])

plate.show()

plate.export_step("outputs/face_plate_with_cutout.step")
