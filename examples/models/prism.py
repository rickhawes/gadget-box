from mini_rack_printables import Assembler, BoxBlock, Rendering


def render() -> Rendering:
    bx = BoxBlock(20, 20, 10)
    asm = Assembler.make_with_block(bx)
    return asm.make_rendering()


rendering = render()
rendering.show()
