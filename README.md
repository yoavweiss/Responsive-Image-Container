# Responsive Image Container

This repo is meant to define how a responsive image format would look
like.
Currently I'm just writing very raw ideas here, so bare with me.

Tha basic principles I have in mind:
* Support image data in multiple formats, and especially WebP, JPEG-XR
  and JPEG.
* Image data will be represented in layers, each layer representing a
  certain resolution.
* The first layer represents the lowest resolution image, and each layer above it
  represents the difference between its resolution and the resolution
below it.
* The container will define a set of algorithms that can be used to
  define the diff calculation between the layers

## Possible algorithms:
* Simple diff - something like [this
  proposal](http://fremycompany.com/BG/2012/Responsive-Image-Protocol-proposal-908/)
can work great for resolution switching
* Placing the lower layer as an image fragment in the layer above it -
  Can be used for art-direction
* Combining the two - to sharpen image fragments
* Is there a case not covered by these two algorithms?

## Container format:
* [RIFF](http://en.wikipedia.org/wiki/Resource_Interchange_File_Format) is the main candidate at the moment, since it's dead simple, and WebP already uses it.

## How will browsers fetch that format?
Wrote this [blog
post](http://blog.yoav.ws/2012/08/Fetching-responsive-image-format) a
while back.


