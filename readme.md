# Gadget Box

A Python library to create a custom box for your gadget. 

As many good models already exist, this project provides more customizilibilty through a library of cutouts and holders with a flexible layout system. The envisioned composible system include:

- Shelves, face plates, and enclosures
- Rectangular and circular cutouts as well as arbritary shapes described an SVG file
- Component holders for common shapes as well as arbritary shapes described in an SVG or STL file


## Example code

To use look at the model and feature packages for existing support devices. Defined the specific
model wanted by adjusting the parameters. 

```python
import gadget_box as gb

#
# This example demonstrates a 10-inch rack faceplate with a 3 network keystone cutouts.
#

# A 1u faceplace with ribs and one row with 3 network keystone cutouts. 
model = gb.render_rack_faceplate(
    rack_units=1.0, 
    style=gb.FaceplateSytle(rib=gb.FaceplateSytle.STD_RIB),
    features=[[gb.Keystone()] * 3]
)

# Show the model in the OCP viewer
model.show()

# Export the model as a STEP file as well
model.export_step("outputs/faceplate_with_keystone.step")
```

## Directory Structure

The project directory structure is as follows:

- `src/gadget_box/` - the main library source code
- `src/gadget_box/models/` - models are the starting point for creating 3d printable models.
- `src/gadget_box/features/` - reusable building blocks that enhance models.
- `src/gadget_box/core` - core code used by models and features
- `src/gadget_box/assets/` - Assets for common 3d printable models in this space. 
- `examples/` - example scripts for creating 3d printable models that use the library
- `scripts/` - scripts for building and testing the library.
- `tests/` - test scripts for verifying the library's functionality
- `outputs/` - directory for storing the output models in STEP or STL format.
- `taskfile.yml` - common task definitions for the project.


 ## TODO

 To make a reasonable library requires

  - [x] Convert to python and build123d
  - [x] WalledHolder, PuckHolder, CornerHolder parts 
  - [x] Shelves
  - [x] ValueErrors instead of asserts
  - [ ] SVG primative 
  - [x] Fill pattern for primatives using intersections
  - [x] Layout redesign with spacers 
  - [x] Holders for shelves
  - [ ] Extract pictures for the readme
  - [ ] Documentation add more examples and usage instructions. Seperated the programming stuff. 
  - [ ] Assembler: bound box
  - [x] Model -> functions
  - [ ] Look at import style standard (consider the google style)
