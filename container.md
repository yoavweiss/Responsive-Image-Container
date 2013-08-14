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
Its value defines the file type. For the Responsive Image container the
value must be "RIC ". Note the space (0x20) at the end.

### ILOT - Image Layer Offset Table

This box will let the decoder know which image resolutions are available
and which offsets these resolutions *end* with.
The goal is that the decoder can then safely fetch only the bytes needed
to display the resolution it needs.
An image must contain an ILOT box.

Internal Fields:
* 2 bytes - image width of the corresponding layer
* 4 bytes - byte offset of the end of the box that contains the corresponding layer

### LBAS - Layer BASe image

The box contains a base image that shold be decoded on its own, without reference to previous images.
For most practical cases, an image should contain one LBAS box, and it
should precede any LAEN boxes (described below).

Internal fields:
* (boxLength - 8) bytes - Image data

### LAEN - LAyer ENhancement
This box contains an enhacement layer &mdash; an image that contitutes
the difference between the previous resolution image and the current
one.
The enhancement can be:
* Higher resolution of an image identical to the previous resolution's
image
* A higher context image than the previous resolution one (i.e. the
previous resolution image is a crop of the current one). It's also
possible that the previous image is rotated.
* The entire layer can be arbitrarily positioned on a transparent
canvas, to enable resolution specific addition to be added as a separate
resource, using a CSS background image.

Internal fields:
* 2 bytes - Display width of the previous layer in current layer
* 2 bytes - Rotate angle of the previous layer, when placed on current layer, in hundredth of a degree (e.g. 180° will be an unsigned int of 18000)
* 2 bytes - X coordinates of the initial position of the previous layer's placement on current layer
* 2 bytes - Y coordinates of the initial position of the previous layer's placement on current layer
* 2 bytes - X coordinates of the initial position of the current layer's placement on the canvas
* 2 bytes - Y coordinates of the initial position of the current layer's placement on the canvas
* (boxLength - 20) bytes - Image data

