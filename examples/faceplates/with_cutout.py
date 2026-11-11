"""Minimal example of a faceplate with a circle cutout feature"""

from mini_rack_printables import CircleFigure, Cutout, FaceplateStyle, rack_faceplate

cutout = Cutout(CircleFigure(10.0), rib=FaceplateStyle.STD_RIB)
plate = rack_faceplate(rack_units=1.0, features=[[cutout, cutout]])

plate.show()

plate.export_step("outputs/face_plate_with_cutout.step")
