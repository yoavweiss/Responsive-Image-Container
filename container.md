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

The box contains a base image that should be decoded on its own, without reference to previous images.
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
previous resolution image is a crop of the current one). 

Internal fields:
* 2 bytes - Display width of the current layer
* 2 bytes - Display height of the current layer
* 2 bytes - X coordinates of the initial position of the previous layer's placement on current layer
* 2 bytes - Y coordinates of the initial position of the previous layer's placement on current layer
* 2 bytes - Numerator of the ratio in which the previous layer should be upscaled
* 2 bytes - Denominator of the ratio in which the previous layer should be upscaled
* (boxLength - 12) bytes - Image data

## How is the container structured?

### File type 
<style>
.box {display: inline-block; border: black solid 1px;box-sizing: border-box;margin: 0;padding: 0;}
.two-bytes {max-width: 100px; width: 15%}
.four-bytes {max-width: 200px; width: 30%}
.infinite-bytes {max-width: 600px; width: 90%}
</style>
<span style="display: inline-block; border: black solid 1px;box-sizing: border-box;margin: 0;padding: 0;" class="box four-bytes">Box len</span><span class="box four-bytes">"FTYP"</span><span class="box four-bytes">"RIC "</span>

### Image Layer Offset Table
<span class="box four-bytes">Box len</span><span class="box four-bytes">"ILOT"</span>

<span class="box two-bytes">width</span><span class="box two-bytes">height</span><span class="box four-bytes">offset</span> x number of layers


### Base Layer
<span class="box four-bytes">Box len</span><span class="box four-bytes">"LBAS"</span>

<span class="box infinite-bytes">Layer data</span>

### Enhancement Layer
<span class="box four-bytes">Box len</span><span class="box four-bytes">"LAEN"</span>

<span class="box two-bytes">width</span><span class="box two-bytes">height</span><span class="box two-bytes">position X</span><span class="box two-bytes">position Y</span><span class="box two-bytes">Numerator</span><span class="box two-bytes">Denominator</span>

<span class="box infinite-bytes">Layer data</span>

