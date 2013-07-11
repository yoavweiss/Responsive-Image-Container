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
* Rotating the lower layer and including it as an image fragement
* Combining all of the above.
* Other???

## Possible container formats:
* [RIFF](http://en.wikipedia.org/wiki/Resource_Interchange_File_Format)
 - Used by WebP
 - Simple
 - Requires the file's size upfront which sucks for on-the-fly file manipulations
* [ISO base media format](http://en.wikipedia.org/wiki/ISO_base_media_file_format)
 - Used by MP4
 - Simple
 - Doesn't require file size upfront
 - Proprietary. Possible licensing issues, but I doubt it.
* [Matroska](http://www.matroska.org/technical/specs/index.html)
 - Used by WebM
 - Not so simple. Highly focused on videos, so it might be a problem to extend it to support images.
 - Doesn't require file size upfront
 - Open & free standard

I've decided to go with an ISO based container, because of its
simplicity, extensibility and the fact that it is streaming friendly.

## How will browsers fetch that format?
Wrote this [blog
post](http://blog.yoav.ws/2012/08/Fetching-responsive-image-format) a
while back.

## Downsides of this solution
If art-directed images of lower resolution are completely different than
their higher resolution counterparts, this solution is no good for that
case. A separate resource would be better there.
