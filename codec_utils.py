from PIL import Image

def getPixels(img):
    img.convert('RGB')
    return list(img.getdata())

def diffImage(highQ, lowQ):
    highQPixels = getPixels(highQ)
    lowQPixels = getPixels(lowQ)
    diffPixels = []
    for h, l in zip(highQPixels, lowQPixels):
        pixel = []
        for i in range(3):
            pixel.append((h[i] - l[i] + 256) / 2)
        diffPixels.append(tuple(pixel))
    diff = Image.new("RGB", highQ.size)
    diff.putdata(diffPixels)
    return diff

def undiffImage(diff, lowQ):
    diffPixels = getPixels(diff)
    lowQPixels = getPixels(lowQ)
    highQPixels = []
    count = 0
    for d, l in zip(diffPixels, lowQPixels):
        pixel = []
        for i in range(3):
            pixel.append((d[i] * 2) - 256 + l[i])
        highQPixels.append(tuple(pixel))
        count += 1
    highQ = Image.new("RGB", diff.size)
    highQ.putdata(highQPixels)
    return highQ

def projectPrevLayerToCurrent(prev, canvasWidth, position, projectionSize, rotateAngle, crop):
    print "projecting", prev.size, crop, position, canvasWidth, projectionSize
    projection = prev.copy()
    # Crop to compensate for lower layer offset
    projection=projection.crop(crop)
    # Rotate the lower layer to match the rotate of the upper layer
    projection=projection.rotate(rotateAngle)
    # Inverse the downsize 
    projection=projection.resize(projectionSize, Image.ANTIALIAS)
    # Inverse crop
    canvas = Image.new('RGBA', canvasWidth, (0, 0, 0, 0))
    canvas.paste(projection, position)
    return canvas

def cropDimensions(crop):
    firstX, firstY, secondX, secondY = crop
    width = secondX - firstX
    height = secondY - firstY
    return width, height
