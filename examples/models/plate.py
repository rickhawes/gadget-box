from mini_rack_printables import (
    Assembler,
    BoxBlock,
    CylinderBlock,
    ExtrudedBlock,
    Model,
    SlotFigure,
    Vec2,
    Vec3,
)


class PlateWithHoles(Model):
    size = Vec3(100, 100, 5)

    def render(self) -> Model.Rendering:
        base = BoxBlock(self.size.x, self.size.y, self.size.z)
        hole = ExtrudedBlock(SlotFigure(10, 5), self.size.z)
        stand = CylinderBlock(5, 10)

        # Assembler is used to assemble this model
        asm = Assembler.make_with_block(base)
        cutout_asm = asm.make_cutout_sub()
        # made with top side as the plane
        asm.place_block(stand, [Assembler.Place(offset=p) for p in self.stand_centers()])

        # place the holes on the base using the cut mode
        cutout_asm.place_block(hole, [Assembler.Place(offset=p) for p in self.hole_centers()])

        return asm.make_rendering()

    def hole_centers(self) -> list[Vec2]:
        dx = self.size.x / 2 - 10
        dy = self.size.y / 2 - 10
        return [Vec2(x, y) for x in [dx, -dx] for y in [dy, 0, -dy]]

    def stand_centers(self) -> list[Vec2]:
        return [Vec2(x, y) for x in [-10, 10] for y in [0]]


rendering = PlateWithHoles().render()
rendering.show()
