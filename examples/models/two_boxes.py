from mini_rack_printables import Assembler, AxDir3, BoxBlock, Dir2, Rendering, Vec3


def render() -> Rendering:
    base = BoxBlock(30, 20, 10)
    node = BoxBlock(2, 1.5, 1)

    # place a node on the side of a box
    asm = Assembler.make_with_block(base, z_dir=AxDir3.Y_MINUS)
    asm.place_block(node, Assembler.Place(origin=Dir2.Y_PLUS))

    return asm.make_rendering()


rendering = render()
rendering.show()
rendering.export_step("outputs/two_boxes.step")
