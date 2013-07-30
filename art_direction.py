from PIL import Image
import algo
import iso_media

"""
{
# canvaswidth - the final layer's dimension width
# imgwidth - The image data dimensions on the final layer
# crop - The final layer's crop from the original image
# position - The image's position on the canvas
# rotate - The image's rotate on the canvas
# Example:
  [ { 'canvaswidth': 300, 
      'imgwidth': 300,
      'crop': (0, 0, 300, 300)},
    { 'canvaswidth': 600,
      'imgwidth': 800,
      'crop': (0, 0, 600, 400),
      'position': (200, 0),
      'rotate': 90} ]
"""

def encode(img, layerParameters):
    if not len(layerParameters):
        return

    def diffImage(highQ, lowQ):
        highQPixels = ResSwitch.Algo.getPixels(highQ)
        lowQPixels = ResSwitch.Algo.getPixels(lowQ)
        diffPixels = []
        for h, l in zip(highQPixels, lowQPixels):
            pixel = []
            for i in range(3):
                pixel.append((h[i] - l[i] + 256) / 2)
            diffPixels.append(tuple(pixel))
        diff = Image.new("RGB", highQ.size)
        diff.putdata(diffPixels)
        return diff

    def createTargetImage(img, parameter):
        target = img.copy()
        # crop the target image from the original image
        target.crop(parameter['crop'])

        # resize it to match the width
        target.thumbnail((parameter['imgwidth'], parameter['imgwidth']), Image.ANTIALIAS)

        # rotate
        target.rotate(parameter['rotate'])

        # position it on the canvas
        width, height = target.size
        posX, posY = parameter['position']
        output = Image.new('RGBA', parameter['canvaswidth'], (0, 0, 0, 0))
        output.paste(target, (posX, posY))
        return output

    def cropDimensions(crop):
        firstX, firstY, secondX, secondY = crop
        width = secondX - firstX
        height = secondY - firstY
        return width, height

    def imgProportion(crop):
        width, height = cropDimensions(crop)
        return height / width

    def projectPrevLayerToCurrent(img, prev, prevParameter, currParameter):
        projection = prev.copy()

        # Crop to compensate for lower layer offset
        posX, posY = prevParameter['position']
        imgWidth = prevParameter['imgWidth']
        imgHeight = imgWidth * imgProportion(prevParameter['crop'])
        projection.crop((posX, posY, posX + imgWidth, posY + imgHeight))

        # Rotate the lower layer to match the rotate of the upper layer
        projection.rotate(prevParameter['rotate'] - currParameter['rotate'])

        # Inverse the downsize 
        # find current layer crop width divided by prev layer's crop width, then inflate
        currWidth = cropDimensions(currParameter['crop'])[0]
        prevWidth, prevHeight = cropDimensions(prevParameter['crop'])
        ratio = float(currWidth)/prevWidth
        projection.resize((prevWidth*ratio, prevHeight*ratio), Image.ANTIALIAS)

        # Inverse crop by finding the lower layer's position on the upper layer
        currCropX0, currCropY0, currCropX1, currCropY1 = currParameter['crop']
        prevCropX0, prevCropY0, prevCropX1, prevCropY1 = prevParameter['crop']
        position = (prevCropX0 - currCropX0, 
                    prevCropY0 - currCropY0)
        output = Image.new('RGBA', currParameter['canvaswidth'], (0, 0, 0, 0))
        output.paste(projection, position)
        return output

    def createLayer(img, parameter, prevLayer, prevLayerParameter):
        targetImg = createTargetImage(img, parameter)
        diff = None

        if prevLayer:
            # Place prev layer on current layer's canvas
            referenceImg = projectPrevLayerToCurrent(img, prevLayer, prevLayerParameter, parameter)

            # Create a diff image
            diff = diffImage(targetImg, referenceImg)
        return targetImg, diff

    layers = []
    prevLayer = None
    for parameter in layerParameters:
        prevLayer, diff = createLayer(img, parameter, prevLayer)
        layers.append((diff or prevLayer, parameter['imgwidth'])

def decode():
    pass

