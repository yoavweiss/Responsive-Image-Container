#Responsive Image Container

It's been a year since I last wrote about it, but the dream of the "magical image format" that will solve world hunger and the responsive image problem (whichever one comes first) lives on.
A few weeks back I started wondering if such an image format can be used to solve both the [art-direction](http://usecases.responsiveimages.org/#art-direction) and [resolution-switching](http://usecases.responsiveimages.org/#resolution-switching) use-cases.

I had a few ideas on how this can be done, so I created a prototype to prove that it's feasible.  This prototype is [now
available](https://github.com/yoavweiss/Responsive-Image-Container) for your tinkering pleasure.

In this post I'll try to explain what this prototype does, what it cannot do, how it works, and what are its downsides. I'll also try to de-unicorn the responsive image format concept, and make it more tangible and less magical.

## Why not a markup solution? You hatin' on markup solutions?

I'm not! Honest. Some of my best friends are markup solutions. 

I've been part of the RICG for a while now, prototyping, promoting and presenting markup solutions.
Current markup solutions (picture *and* srcset) are great and can cover all the important use cases for responsive images, and if it was up to me, I'd vote for shipping both picture and srcset (in its resolution switching version) in all browsers tomorrow.

*But* the overall markup based solution has some flaws.

Here's some of the criticism I've been hearing for the last year or so when talking responsive images markup solutions.

### They're too verbose

Markup solution are by definition verbose, since they must enumerate all the various resources. When art-direction is involved, they must also state the breakpoints, which adds to that verbosity.

### They're mixing presentation and content

Art-direction markup solution needs to keep layout breakpoints in the markup. That mixes presentation and content, and means that layout changes will force markup changes.

There have been [constructive discussions](http://lists.w3.org/Archives/Public/www-style/2013May/0638.html) on how this can be resolved, by bringing back the MQ definitions into CSS, but it's not certain when any of this will be defined and implemented.

### They define breakpoints according to the viewport

This one is heard often from developers. For performance reasons, markup based solutions are based on the viewport size, rather than on the image's dimensions. 
Since the images' layout dimensions are not yet known to the browser by the time it start fetching images, it cannot rely on them to decide which resource to fetch.  

For developers, that means that some sort of "viewport=>dimensions" table needs to be created on the server-side/build-step or inside the developer's head in order to properly create images that are ideally sized for a certain viewport dimensions and layout.

While a build step can resolve that issue in many cases, it can get complicated in cases where a single components is used over multiple pages, with varying dimensions in each.

### They may result in excessive download in some cases

OK, this one is something I hear mostly in my head (and from other Web performance freaks on occasion).

From a performance perspective, any solution that's based on separate resources for different screen sizes/dimensions requires re-downloading of the entire image if the screen size or dimensions change to a higher resolution than before.  Since it's highly possible that most of that image data is already in the browser's memory or cache, re-downloading everything from scratch makes me sad.


All of the above made me wonder (again) how wonderful life would be if we had a file format based solution, that can address these concerns.

## Why would a format based solution do better?

* The burden is put on the image encoder. The markup stays identical to what it is today. A single tag with a single resource.
* Automated conversion of sites to such a responsive images solution may be easier, since the automation layer would just focus on the images themselves rather than the page's markup and layout.
* Image layout changes (following viewport dimension changes) can be handled by downloading only the difference between current image and the higher resolution one, without re-downloading the data that the browser already has in its memory.
* Web developers will not need to maintain multiple version of each image resource, even though they would have to keep a non-responsive version of the image, for content negotiation purposes.

This is my attempt at a simpler, file format based solution that will let Web developers do much less grunt work, avoid downloading useless image data (even when conditions change), while keeping preloaders working.

## Why not progressive JPEG?
Progressive JPEG can [fill this role](http://blog.yoav.ws/2012/05/Responsive-image-format) for the resolution switching case, but it's extremely rigid. There are strict limits on the lowest image quality, and from what I've seen, it is often too data-heavy. The minimal difference between resolutions is also limited, and doesn't leave enough control to encoders that want to do better.
Furthermore, progressive JPEG cannot do art-direction at all.

## So, how would this file format of yours looks like?
A responsive image container, containing internal layers that can be either WebP, JPEG-XR, or any future format. It uses resizing and crop operations to cover both the resolution switching and the art direction use cases. 

The decoder (e.g. the browser) will then be able to download just the number of layers it needs (and their bytes) in order to show a certain image. Each layer will provide enhancement on the layer before it, giving the decoder the data it needs to show it properly in a higher resolution.

## How does it work?

* The encoder takes the original image, along with a description of the required output resolutions and optionally art-direction directives.
* It then outputs a layer per resolution that the final image should be perfectly rendered in.
* Each layer represents the difference in image data between the previous layer, when "stretched" on the current layer's canvas, and the current layer's "original" image. That way, the decoder can construct the layers one by one, each time using the previous layer to recreate the current one, creating a higher resolution image as it goes.

Support for resolution switching is obvious in this case, but art-direction can also be supported by positioning the previous layer on the current one and being able to give it certain dimensions.

Let's look at some examples, shall we:


### Art-direction 
Here's a photo that used often in discussion of the art-direction
use-case (I've been too lazy to search for a new one):

![Obama in a jeep factory - original with context](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/crop.jpg)

let's take a look at what the smallest layer would look like:

![Obama in a jeep factory - cropped to show only
Obama](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/crop.jpg_layer1.webp.png)

That's just a cropped version of the original - nothing special.

Now one layer above that:

![Obama in a jeep factory - some context + diff from previous
layer](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/crop.jpg_layer2.webp.png)

You can see that pixels that don't appear in the previous layer are
shown normally, while pixels that do only contain the difference between
them and the equivalent ones in the previous layer.

And the third, final layer:

![Obama in a jeep factory - full context + diff from previous
layer](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/crop.jpg_layer3.webp.png)

### Res switching 

The original resolution photo of a fruit:
![iPhone - original
resolution](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/res_switch.png)

The first layer - showing a significantly downsized version
![iPhone - significantly
downsized](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/res_switch.png_layer1.webp.png)

The second layer - A diff between a medium sized version and the
"stretched" previous layer
![iPhone - medium sized
diff](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/res_switch.png_layer2.webp.png)

And the third layer - containing a diff between the original and the
"stretched" previous layer
![iPhone - full sized
diff](https://raw.github.com/yoavweiss/Responsive-Image-Container/blog_post/samples/test_results/res_switch.png_layer3.webp.png)

If you're interested in more details you can go to the [repo](https://github.com/yoavweiss/Responsive-Image-Container). More details on the [container's structure] are also there.

### But I need more from art-direction
I've seen cases where rotation and image repositioning is required for art-direction cases. It was usually in order to add a logo/slogan at different locations around the image itself, depending on the viewport dimensions.

This use-case is probably better served by CSS. CSS transforms can handle rotation and CSS positioning, along with media specific background images, can probably handle the rest.

If your art-direction case is special, and can't be handled by either one of those, I'd love to hear about it.

## How will it be fetched?

That's where things get tricky. A special fetching mechanism must be created in order to fetch this type of images. I can't say that I have that part all figured out, but here's my rough idea on how it may work.

My proposed mechanism relies on HTTP ranges, similar to the fetching mechanisms of the <video> element, when seeks are involved.

More specifically:

* Resources that should be fetched progressively should be flagged as such. One possibility is to add a `progressive` attribute on the element describing the resource.
* Once the browser detects an image resource with a `progressive` attribute on it, it picks the initial requested range for that resurce. The initial range request can be any one of either:
 - A relatively small fixed range for all images
 - Specified by the author (e.g. as a value of the `progressive` attribute)
 - Some heuristic
 - Based on a manifest (we'll get to that later)  
* The browser can fetch this initial range at the same time it requests the entire resource today, or even sooner, since the chances of starving critical path resources (e.g. CSS & JS) are slimmer.
* Once the browser has downloaded the image's initial range, it has the file's offset table box, which links byte offset to resolution.  That means that once the browser has layout, it'd know exactly which byte range it needs in order to display the image correctly.
* Assuming the browser sees fit, it can heuristically fetch followup layers(i.e. higher resolutions), even before it knows for certain that they are needed.
* Once the browser has the page's layout, it can complete fetching of all the required image layers.

The above mechanism will increase the number of HTTP requests, which in an HTTP/1.1 world will probably introduce some delay in many cases.
That mechanism can be optimised by defining a manifest that would describe the image resources' bytes ranges to the browser.
The idea for adding a manifest was proposed by [Cyril Concolato] at last year's TPAC, and it makes a lot of sense, borrowing from our collective experince with video streaming. It can enable browsers to avoid fetching an arbitrary initial range (at least once the manifest was downloaded itself).
Adding a manifest will prevent these extra requests for everything requested after layout, and may help to prevent them (using heuristics) even before layout.

Creating a manifest can be easily delegated to either build tools or the server side layer, so devs don't have to manually deal with these image
specific details.

### Can't we simply download the image and reset the connection once the browser had enough?
No, since that will likely introduce serious performance issues.
The problem with reseting a TCP connection during a browsing session are:

* It terminates an already connected, warmed up TCP connection which setup had a significant performance cost, and that could have be re-used for future resources.
* It, by definition, sends at least an RTT worth of data down the pipe, the time it takes for the browser's reset to reach the server. That data is never read by the browser, which means wasted bandwidth.

## What are the downsides of this approach?

* It involves touching and modifying many pieces of the browser stack, which means that standardization and implementation may be more painful
* The monochrome/print specific images cannot be addressed by this type of a solution. While this is not a major use-case, this is a downside.
* The decoding algorithm involves a per-layer upscaling process, which may be heavy. Therefore, decoding performance may be an issue. Moving this to the GPU may help, but I don't know that area well enough to be the judge of that. If you have an opinion here, please comment. 
* Introducing a new file format is a painful and long process. As we have seen with the introduction of past image formats, the lack of a
  client-side mechanism makes this a painful process for Web developers. Since new file formats start out being supported in some browsers but not others, a server-side mechanism must be used (hopefully based on the Accept header, rather than on UA). I'm hoping that the fact that this new file format is very simple, and relies on other file formats to do the heavy lifting, may help here, but I'm not sure it would.
* As discussed above, it's likely to increase the number of requests, and may introduce some delay in HTTP/1.1
* This solution cannot answer the need for "pixel perfect" images, which is mainly needed to improve decoding speed. Even if it would, as we
  said about, decoding speed is a concern.
* Relying on HTTP ranges for the fetching mechanism can result in some problem with intermediate cache server, which don't support it.

## So, should we dump markup solutions?
Not at all. This is a prototype, showing how most of the responsive images use-cases would have been solved. Reaching consensus on this solution, defining it in detail and implementing it in an interoperable way may be a long process. The performance implication on HTTP/1.1 sites still needs to be explored.
I believe this may be a way to simplify responsive images in the future, but I don't think we should wait for the ideal solution. 

## Summary
If you just skipped here, that's OK. It's a long post.

Just to sum it up, I've demonstrated (along with a prototype) how a responsive image format can work, and can resolve most of the responsive images use cases. I also went into some details about which other bits would have to be added to the platform in order to make it a viable solution.

I consider this solution to be a long term solution since some key issues need to be addressed before this solution can be practical.  
IMO, the main issue is decoding performance, with download performance impact on HTTP/1.1 is a close second.

I think it's worth while to continue to explore this option, but not wait for it. Responsive images need an in-the-browser, real-life solution <del>Two years ago</del> today, not two years from now.

