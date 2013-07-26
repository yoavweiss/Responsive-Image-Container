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

### ILDT - Image Layer DaTa

The payload of the layer. Basically the image data.

### LBAS - Layer Base image

Indicates that the following box will contain a base image that should
be decoded on its own, without reference to previous images.

### LAHD - Layer Algorithm Higher Definition

Indicates that the following box will contain an image that is an
enhancement layer to the images that preceded it. 

### LACR - Layer Algorithm CRop

TBD

### LART - Layer Algorithm RoTate

TBD

### LAPR - Layer Algorithm PaRtial

TBD


