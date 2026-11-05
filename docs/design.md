# Software Design

## Concepts

Block constructions - A model is constructed using blocks placed on other blocks. An assembler class assists in placing blocks on other blocks. 

## Layers

The package is built into three layers: Core primatives and Models built on those core primatives. 


| Layer    | Abstractions                                                  | Knowledge Needed   |
| -------- | ------------------------------------------------------------- | ------------------ |
| Example  | Actual devices and jobs                                       | models, core       |
| Models   | Models for devices                                            | core               |
| Features | Features for models                                           | core               |
| Core     | Primitives to build models. Wraps build123d for model makers. | build123d          |


## Concepts

Models are 

A model is constructed using blocks placed on other blocks. An assembler class assists in placing
blocks on other blocks. 

## Terminology 

Names are chosen to not overlap the names used in build123. 

- x, y, z - coordinates in space.
- model - a model that is stands on its own.
- feature - a feature is a feature on a plate that can be added or subtracted from the model's geometry.
- size - a [dx, dy] or a [dx, dy, dz] vector with dimensions of a volume 2d or 3d. Always positive.
- plate - a flat area of model where features can be placed.
- section - the section of a plate that holds a feature.
- padding - a single distance for an outset, always positive.
- figure - a 2-d outline primative used to build blocks
- block - a 3-d primiative for building models
- rc - A size [dx, dy] and [x, y] vectors defining a 2d area in space.
- bx - A 3d equivalent for 
- rib - A rib outlines a 2d area on a plate for extra strength. It has depth and width.

## Coordinates

Models are oriented for 3d printing. They are centered in the XY plane and with block placed in the positive Z direction. 

Terms like `width`, `height`, `depth`, `top`, `bottom`, `front`, `back`, `left`, `right` are used in reference to this XYZ orientation. In other words, `left` refers to the negative X direction, `right` refers to the positive X direction, and so on. 