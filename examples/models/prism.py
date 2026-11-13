"""Make  a box with an assembler."""

from gadget_box import Assembler, BoxBlock

bx = BoxBlock(20, 20, 10)
asm = Assembler.make_with_block(bx)
rendering = asm.make_rendering()
rendering.show()
