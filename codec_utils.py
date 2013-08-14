from PIL import Image

def getPixels(img):
    img.convert('RGBA')
    return list(img.getdata())

def diffImage(highQ, lowQ):
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

def projectPrevLayerToCurrent(prev, canvasWidth, position, projectionSize, rotateAngle, crop):
    print "projecting", prev.size, crop, position, canvasWidth, projectionSize
    projection = prev.copy()
    # Crop to compensate for lower layer offset
    projection=projection.crop(crop)
    # Inverse the downsize 
    projection=projection.resize(projectionSize, Image.ANTIALIAS)
    # Rotate the lower layer to match the rotate of the upper layer
    print "rotating", rotateAngle, projection.size
    projection=projection.rotate(rotateAngle)
    # Inverse crop
    canvas = Image.new('RGBA', canvasWidth, (0, 0, 0, 0))
    canvas.paste(projection, position)
    return canvas

def cropDimensions(crop):
    firstX, firstY, secondX, secondY = crop
    width = secondX - firstX
    height = secondY - firstY
    return width, height
