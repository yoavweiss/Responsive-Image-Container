from PIL import Image

def getPixels(img):
    img = img.convert('RGBA')
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
        if l[3]>0:
            for i in range(4):
                pixel.append((d[i] * 2) - 256 + l[i])
            highQPixels.append(tuple(pixel))
        else:
            highQPixels.append(d)
        count += 1
    highQ = Image.new("RGBA", diff.size)
    highQ.putdata(highQPixels)
    return highQ

def cropDimensions(crop):
    firstX, firstY, secondX, secondY = crop
    width = secondX - firstX
    height = secondY - firstY
    return width, height

def projectPrevLayerToCurrent(prev, canvasDimensions, position, ratio):
    projection = prev.copy()
    ratiores = float(ratio[0]) / ratio[1]
    # Inverse the downsize 
    upscale_size = tuple([int(x*ratiores) for x in projection.size])
    projection=projection.resize(upscale_size, Image.ANTIALIAS)
    # Inverse crop
    canvas = Image.new('RGBA', canvasDimensions, (0, 0, 0, 0))
    canvas.paste(projection, position)
    return canvas

def gcd(a, b):
    if a < b:
        a, b = b, a

    while b > 0:
        t = b
        b = a % t
        a = t
    return a

