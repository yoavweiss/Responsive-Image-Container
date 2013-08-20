from PIL import Image

counter = 0

def getPixels(img):
    img.convert('RGBA')
    return list(img.getdata())

def diffImage(highQ, lowQ):
    if lowQ.size > highQ.size:
        lowQ=lowQ.crop((0,0,highQ.size[0], highQ.size[1]))
    highQPixels = getPixels(highQ)
    lowQPixels = getPixels(lowQ)
    diffPixels = []
    for h, l in zip(highQPixels, lowQPixels):
        pixel = []
        if l[3]>0:
            for i in range(4):
                pixel.append((h[i] - l[i] + 256) / 2)
            diffPixels.append(tuple(pixel))
        else:
            diffPixels.append(h)
    diff = Image.new("RGBA", highQ.size)
    diff.putdata(diffPixels)
    return diff

def undiffImage(diff, lowQ):
    diffPixels = getPixels(diff)
    lowQPixels = getPixels(lowQ)
    highQPixels = []
    count = 0
    for d, l in zip(diffPixels, lowQPixels):
        pixel = []
        for i in range(4):
            pixel.append((d[i] * 2) - 256 + l[i])
        highQPixels.append(tuple(pixel))
        count += 1
    highQ = Image.new("RGBA", diff.size)
    highQ.putdata(highQPixels)
    return highQ

def cropDimensions(crop):
    firstX, firstY, secondX, secondY = crop
    width = secondX - firstX
    height = secondY - firstY
    return width, height

def projectPrevLayerToCurrent(prev, canvasWidth, position, rotateAngle, crop, ratio):
    global counter
    counter += 1
    projection = prev.copy()
    # Crop to compensate for lower layer offset
    if cropDimensions(crop) < prev.size:
        projection=projection.crop(crop)
        projection.save("/tmp/crop"+str(counter)+".webp", "WEBP")
    # Inverse the downsize 
    upscale_size = tuple([int(x*ratio) for x in projection.size])
    print "upscale", upscale_size
    print "Here upscaling screws up rotate since the dimensions are fucked"
    projection=projection.resize(upscale_size, Image.ANTIALIAS)
    projection.save("/tmp/upscale"+str(counter)+".webp", "WEBP")
    # Rotate the lower layer to match the rotate of the upper layer
    projection=projection.rotate(rotateAngle)
    projection.save("/tmp/rotate"+str(counter)+".webp", "WEBP")
    # Inverse crop
    canvas = Image.new('RGBA', canvasWidth, (0, 0, 0, 0))
    canvas.paste(projection, position)
    return canvas

