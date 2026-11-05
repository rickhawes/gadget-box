# Dev Notes

## Choices 

The project was originally coded in OpenSCAD and BOSL2 which is a common choice in the 3d printing community, but was ported to Python for better software development tools like tests and language features like classes. [build123d](https://github.com/build123d/build123d) was selected for base framework because it has good documentation and an intuitive API for creating 3d models after trying CadQuery. Every tool and framework choice has its trade-offs, but these choices ended up being the best for the author's enjoyment. 

## Python Style Guide

Type hinting is great help for Python projects, especially with many different types. The choice of the PyReFly, with its aggressive type inference, for the LSP for the project reflects this preference.

Choices:

- PyReFly for the LSP
- Black for formatting
- Google Python Style guide


## Coordinates

Models are oriented for 3d printing. They are centered in the XY plane and with solids extruded in the positive Z direction. This is the default of build123d library. Parts are centered in the local coordinate in the XY plane as well. 

Terms like `width`, `height`, `depth`, `top`, `bottom`, `front`, `back`, `left`, `right` are used in reference to this XYZ orientation. In other words, `left` refers to the negative X direction, `right` refers to the positive X direction, and so on. 

## Naming Conventions

Terms commomly used in the project

- x, y, z - coordinates in space.
- model - a model that is stands on its own.
- feature - a feature that can be added to a model
- size - a [dx, dy] or a [dx, dy, dz] vector with dimensions of a volume 2d or 3d. Always positive.
- plate - a flat area of a model that can hold features
- section - the section of a plate that holds a part.
- padding - a single distance for an outset, always positive.
- rc - A pair of size [dx, dy] and [x, y] vector defining a 2d area in space.
- rib - A rib outlines a 2d area on a plate for extra strength. It has depth and width.

