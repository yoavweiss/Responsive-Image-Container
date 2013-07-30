# Container structure

The container is based on the [ISO base media container](http://en.wikipedia.org/wiki/ISO_base_media_file_format).

## Overall structure
The container is built from "boxes" where each box represents an independant unit, with its own internal structure. All the boxes that are not common to all ISO based media containers (everything besides FTYP), will be defined below.

Each box is structured as:
* a 4 byte length indicator (length includes the indicator's length)
* a 4 byte box name
* The box's payload

All values in the container are big-endian unsigned integer values, unless stated otherwise.

## Box types

### FTYP - File type box 
Standard and common to all ISO media files
Its value defines the file type. For the Responsive Image container the value must be "RIC "

### ILOT - Image Layer Offset Table

This box will let the decoder know which image resolutions are available and which offsets these resolutions *end* with
The goal is that the decoder can then safely fetch only the bytes needed to display the resolution it needs

Internal Fields:
* 2 bytes - image width of the corresponding layer
* 4 bytes - byte offset of the end of the box that contains the corresponding layer

### ILXT - Image Layer eXtended offset Table

Similiar to ILOT, but with larger field sizes, for extremely large images

Internal Fields:
* 4 bytes - image width of the corresponding layer
* 8 bytes - byte offset of the end of the box that contains the corresponding layer

### LBAS - Layer Base image

The box contains a base image that shold be decoded on its own, without reference to previous images.

Internal fields:
* (boxLength - 8) bytes - Image data

### LAHD - Layer Algorithm Higher Definition

The box contains contains an image that is an enhancement layer to the images that preceded it. 

Internal fields:
* (boxLength - 8) bytes - Image data

### LACR - Layer Algorithm CRop

ALL WE NEED IS CROP. Naa na na na na
Add crop to this layer, simplifying it significantly

The "logo on the side" thing can be acheived by alpha transparency and a
background image

The bow contains an image that is the difference image between the
preceding layer image, placed somewhere on the current resolution
canvas, and the current one ?????????????????????????? Use words
!!!!!!!!

Internal fields:
2 bytes - Width of the previous layer's crop 
2 bytes - Height of the previous layer's crop 
2 bytes - X coords of the previous layer's crop 
2 bytes - Y coords of the previous layer's crop  
2 bytes - Width of the previous layer inside this layer
2 bytes - Height of the previous layer inside this layer
2 bytes - X coords of the previous layer inside this layer
2 bytes - Y coords of the previous layer inside this layer
2 bytes - Rotate angle of previous layer inside this layer
(boxLength - 26) bytes - Image data


