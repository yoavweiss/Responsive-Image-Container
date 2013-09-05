C I G F L

#Layered Enhancement Image Container

It's been a year since I last wrote about the "magical image format" solution to the responsive images problem. A few weeks back I started wondering if such an image format can also solve the art-direction use-case, as well as the resolution switching use case.  I had a few ideas on how this can be done, so I created a prototype to prove that it's feasible.  This prototype is [now
available](https://github.com/yoavweiss/Responsive-Image-Container) for your tinkering pleasure.

In this post I'll try to explain what this prototype does, how it works, and what cases can't it resolve.

## Why bother with an image format?
An image format poses a few advantages on the current suggested proposals:
* It doesn't require any markup changes 
 - Making it easy to deploy in existing sites
 - Doesn't mix image resource information inside the content layer
 - Requires no server side logic 
 - Can respond to browser environment changes (for example an
   orientation change that requires a larger image) by downloading only
   the layers that are required, instead of downloading the entire image
   all over again.

It also has a few obvious disadvantages:
* File format adoption is hard
 - Introducing new file formats to the Web platform is hard, especially for content images which have no client-side fallback mechanism
* Some use cases can't be addressed by it
 - I'll touch on that point layer
* It involves touching and modifying many pieces of the browser stack, which means that standardization and implementation may be more painful

At least regarding the adoption part, I've tried to tackle it by not trying to come up with new types of encoding, but to use existing file formats (WebP, and JPEG-XR) as the encoding format, and simply create a wrapper around them, so that IP and patents issues (which I believe are a big factor is hindering adoption of new formats) would be minimal.

## Why you hatin' on markup solutions?
I'm not! Honest. Some of my best friends are markup solutions. I've been part of the RICG for a while now, prototyping, promoting and presenting markup solutions.

Current markup solutions (picture+srcset) are great and can cover all the important use cases for responsive images, and if it was up to me, I'd vote for implementing both picture and srcset (in its resolution switching version) in all browsers tomorrow.

*But* the overall markup based solution is not perfect.

Here's what I've been hearing for the last year or so when talking responsive images markup solutions.

### They're too verbose
Markup solution are by definition verbose, since they must enumerate the various resources. When art-direction is involved, they must also state the breakpoints, which adds to that verbosity.

### They're mixing presentation and content
Keeping image layout breakpoints in the markup, which art-direction obliges us to do, mixes presentation and content, and means that layout changes will force markup changes.

### They define breakpoints according to the viewport
This one is heard often from developers. For performance reasons, markup based solutions are based on the viewport size, rather than on the image's dimensions. 
Since the images' layout dimensions are not yet known to the browser by the time it start fetching images, it cannot rely on them to decide which resource to fetch.  
For developers, that means that some sort of "viewport=>dimensions" table needs to be created on the server-side/build-step or inside the developer's head in order to properly create images that are ideally sized for a certain viewport dimensions and layout.

While a build step can resolve that issue in many cases, it can get complicated in cases where a single components is used over multiple pages, with varying dimensions in each.

### They may result in excessive download in some cases
OK, this one is something I hear mostly in my head (and from other Web performance freaks on occasion).

From a performance perspective, any solution that's based on separate resources for different screen sizes/dimensions, requires redownloading of the entire image if the screen size or dimensions change to a higher resolution than before.  Since it's highly possible that most of that image data is already in the browser's memory or cache, redownloading everything from scratch makes me sad.

All of the above made me wonder (again) if we won't do better with a file format based solution, that can address some of these concerns.

## Why would a format based solution do better?
Several of the issues stated above can be improved by a file format based solution:

* The burden is put on the image encoder. The markup stays identical to what it is today. A single tag with a single resource.
* Small developers can continue to host static files, like they always did.
* Building an automatic optimization layer may be easier, since it would just focus on the images themselves rather than the page's layout.
* Viewport size and changes to image dimensions can be handled by downloading an extra layer, without re-downloading the data that the browser already has in its memory.

This is my attempt at a simpler, file format based solution that will let authors do much less grunt work, avoid downloading useless image data (even when conditions change), while keeping preloaders working.

## So, how would a file format solution look like?
A responsive image container, containing internal layers that can be either WebP, JPEG-XR, or any future format. It uses resizing and crop operations to cover both the resolution switching and the art direction use cases. 

The decoder (e.g. the browser) will then be able to download just the number of layers it needs (and their bytes) in order to show a certain image. Each layer will provide enhancement on the layer before it, giving the decoder the data it needs to show it properly in a higher resolution.

## How does it work?
The encoder takes the original image, along with a description of the required output resolutions and optionally art-direction directives.
It then outputs a layer per resolution that the final image should be perfectly rendered in.
Each layer represents the difference in image data between the previous layer, when "stretched" on the current layer's canvas, and the current layer's "original" image. That way, the decoder can construct the layers one by one, each time using the previous layer to recreate the current one, creating a higher resolution image as it goes.

Support for resolution switching is obvious in this case, but art-direction can also be supported by positioning the previous layer on the current one and being able to give it certain dimensions.

I know I just said a lot of words that don't necessarily make a whole lot of sense, so here are some examples:

Res switching example !!!
[iPhone]
[iphone thumbnail]
[second layer]

Art-direction example !!!
[Obama in a jeep factory]

[First Layer]

[ Second layer]

[Third, final layer]

If you're interested in more details you can go to the [repo]. More details on the [container's structure] are also there.

### But I need more from art-direction
I've seen cases where rotation and image repositioning is required for
art-direction cases. It was usually in order to add a logo/slogan at
different locations around the image itself, depending on the viewport
dimensions.

This use-case is most probably better served by CSS. CSS transforms can handle rotation and CSS positioning,
along with media specific background images, can probably handle the rest.

If your art-direction case is special, and can't be handled by either
one of those, I'd love to hear about it.

## How will it be fetched?

That's where things get tricky. A special fetching mechanism must be created in order to fetch this type
of images. I can't say that I have that part all figured out, but here's
my rough idea on how it may work.

My proposed mechanism relies on HTTP ranges, similar to the fetching
mechanisms of the <video> element, when seeks are involved.

More specifically:
* Resources that should be fetched progressively should be flagged as
  such. One possibility is to add a `progressive` flag on the element
  describing the resource.
* The browser can then request these resource's initial range, instead
  of the entire resource. The initial range request can be either a
  relatively small fixed range for all images, specified by the author (e.g. as a value of the
  `progressive` attribute), some heuristic, or based on a manifest (we'll get to that later).
  The browser can fetch this initial range at the same time it today
  requests the entire resource, or even sooner, since the chances of
  starving critical path resources (e.g. CSS & JS) are slimmer.
* Once the browser has the image's initial range, it has the ILOT box,
  which contains an offset table which links byte offset to resolution.
  That means that once the browser has layout, it'd know exactly which
  byte range it needs to display the image correctly.
* Assuming the browser sees fit, it can heuristically fetch followup
  layers, even before it has layout.
* Once the browser has layout, it can complete fetching of all the required image
  layers.

That mechanism can be optimised by defining a manifest that
would describe the image resources' bytes ranges to the browser.
That idea was proposed by [Cyril Concolato] at last year's TPAC,
and it makes sense. I can enable browsers to avoid fetching an arbitrary
initial range (at least once the manifest was downloaded itself).

The above mechanism will increase the number of HTTP requests, which in
an HTTP/1.1 world will probably introduce some delay in many cases.
Adding a manifest will prevent these extra requests for everything
requested after layout, and may help to prevent them (using heuristics)
even before layout.

Creating a manifest can be easily delegated to either build tools or the
server side layer, so devs don't have to manually deal with these image
specific details.

### Can't we simply download the image and reset the connection once the browser had enough?
No, since that will likely introduce seroius performance issues.
The problem with reseting a TCP connection during a browsing session are:
* It terminates an already connected, warmed up TCP connection which
  setup had a significant performance cost, and that could have be
  re-used for future resources.
* It, by definition, sends at least an RTT worth of data down the pipe,
  the time it takes for the browser's reset to reach the server. That
  data is never read by the browser, which means wasted bandwidth.

## Caveats of this approach
* The monochrome/print specific images cannot be addressed by this type
  of a solution. While this is not a major use-case, this is a downside.
* The decoding algorithm involves a per-layer upscaling process, which may be heavy. Therefore, decoding performance may be an
  issue. Moving this to the GPU may help, but I don't know that area well
  enough to be the judge of that. If you have an opinion here, please comment. 
* Introducing a new file format is a painful and long process. As we
  have seen with the introduction of past image formats, the lack of a
  client-side mechanism makes this a painful process for Web developers. 
  Since new file formats start out being supported in some browsers but not others,
  a server-side mechanism must be used (hopefully based on the Accept header, rather than on UA). I'm hoping that the fact that this new file format is very simple, and relies on other file formats to do the heavy lifting, may help here, but I'm not sure it would.
* As discussed above, it's likely to increase the number of requests, and may introduce some delay in HTTP/1.1
* This solution cannot answer the need for "pixel perfect" images, which
  is mainly needed to improve decoding speed. Even if it would, as we
  said about, decoding speed is a concern.
* Relying on HTTP ranges for the fetching mechanism can result in some
  problem with intermediate cache server, which don't support it.

## So, should we dump markup solutions?
Not at all. This is a prototype, showing how most of the responsive
images use-cases would have been solved. Reaching consensus on this solution , defining it in detail and implementing it in
an interoperable way may be a long process. The performance implication
in HTTP/1.1 sites still needs to be explored.
I believe this may be a way to simplify responsive images in the future,
but I don't think we should wait for the ideal solution. 

This is a very early prototype of what such a thing would look like. It
may be better, but I don't think it's worth waiting for it.




VIn order to do that, the format will have to create resolution specific
layers, that can then be re-positioned and resized in order to create a
reference frame for the new resolution specific layer.
In the last few weeks I've been spending my evenings working on
prototyping an image format. An image format (a container, really) that
will allow arbitrary layering of various resolutions and crops of a
single image, in a way that would enable a browser to download only a
range of bytes from the file's top to display the image dimensions it
needs display.


* Layer cleanness - Keeping information on the various resources of an
  image inside the markup tends to break layer boundaries.
 but have received justified
criticism by authors for being too verbose. 
The major downside of markup solutions is that they include the resource URLs as part of the markup,
which mixes layout with markup, and creates maintenance burden when the
images change. It can be improved by placing some server side system in
place that manages it, but:

* requiring a server side excludes a large part of the small web
  developers, that can't have such an access to their servers
* it violates layering when image Shorewood info becomes part of the
  markup, ideally we'd want all image info to be contained as part of
  the image
* designing a server side system that automates picture can very quickly
  become an extremely complicated task. Since a single image can be viewed
  with different dimensions from different templates, complexity adds up quickly.

Initially, I thought a build step can overcome these obstacles, but I'm
becoming more and more convinced that in the world of Web components,
this will not do. A dynamic solution must handle that, at least of these
Web Components are responsive and embedded at varying resolutions.
While declarative Web Components are not yet feasible, they will be.
Leaving them out if not a good idea.

