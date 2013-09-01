# Responsive Image Container

This repo specifies and prototypes a new responsive image container.

## The basic principles:

* Support image data in multiple formats, and especially WebP & JPEG-XR.
* Image data will be represented in layers, each layer representing a
  certain resolution.
* The first layer represents the lowest resolution image, and each layer above it
  represents the difference between its resolution and the resolution
below it.
* The container will define a set of algorithms that can be used to
  define the diff calculation between the layers

## Algorithms:

* Simple diff - something like [this
  proposal](http://fremycompany.com/BG/2012/Responsive-Image-Protocol-proposal-908/)
can work great for resolution switching
 - Maybe can be extended with better extrapolation algorithms, such as
   [this
one](http://www.wisdom.weizmann.ac.il/~vision/SingleImageSR.html)
* Placing the lower layer as an image fragment in the layer above it -
  Can be used for art-direction

## Container format:

After hesitating between [RIFF](http://en.wikipedia.org/wiki/Resource_Interchange_File_Format), 
[Matroska](http://www.matroska.org/technical/specs/index.html) and 
[ISO base media format](http://en.wikipedia.org/wiki/ISO_base_media_file_format), 
I've decided to go with the ISO media format, because of its
simplicity, extensibility and the fact that it is streaming friendly,
(the entire file's size is not required before writing the file's
header).

## How will browsers fetch that format?

Wrote this [blog
post](http://blog.yoav.ws/2012/08/Fetching-responsive-image-format) a
while back.

## Downsides of this solution

* Decoding of this container will consume more than traditional
  sequantial JPEGs, since it'd require layer compositing. 
 - This may be eased by using the GPU for compositing.
* If art-directed images of lower resolution are completely different than
their higher resolution counterparts, this solution is no good for that
case. 
 - A separate resource would be better there.
 - There seems to be a consensus that this case is rather rare.
