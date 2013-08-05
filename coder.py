from PIL import Image
import algo
import iso_media

from codec_utils import diffImage, projectPrevLayerToCurrent
from config_reader import LayerConfig


def encode(img, config):
    if not len(config):
        return

    def createTargetImage(img, parameter):
        target = img.copy()
        # crop the target image from the original image
        target.crop(parameter.crop)

        # resize it to match the width
        target.thumbnail((parameter.img_width, parameter.img_width), Image.ANTIALIAS)

        # rotate
        target.rotate(parameter.rotate)

        # position it on the canvas
        width, height = target.size
        posX, posY = parameter.position
        output = Image.new('RGBA', parameter.canvas_dimensions, (0, 0, 0, 0))
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

    def projectPrevLayerParametersToCurrent(prevLayerConfig, currLayerConfig):
        # Calculate the previous layer's crop, to compensate for offset
        posX, posY = prevLayerConfig.position
        imgWidth = prevLayerConfig.img_width
        imgHeight = imgWidth * imgProportion(prevLayerConfig.crop)
        crop = (posX, posY, posX + imgWidth, posY + imgHeight)

        # calculate the rotate angle difference
        rotateAngle = prevLayerConfig.rotate - currLayerConfig.rotate
        if rotateAngle < 0:
            rotateAngle += 360

        # find current layer crop width divided by prev layer's crop width,
        # to get the dimensions to which we need to inflate the previous layer
        currWidth = cropDimensions(currLayerConfig.crop)[0]
        prevWidth, prevHeight = cropDimensions(prevLayerConfig.crop)
        ratio = float(currWidth)/prevWidth
        projectionSize = (int(prevWidth*ratio), int(prevHeight*ratio))

        # Find the lower layer's position on the upper layer, to inverse the crop
        currCropX0, currCropY0, currCropX1, currCropY1 = currLayerConfig.crop
        prevCropX0, prevCropY0, prevCropX1, prevCropY1 = prevLayerConfig.crop
        position = (prevCropX0 - currCropX0, 
                    prevCropY0 - currCropY0)
        return currLayerConfig.canvas_dimensions, position, projectionSize, rotateAngle, crop

    def createLayer(img, layerConfig, prevLayer, prevLayerConfig):
        targetImg = createTargetImage(img, layerConfig)
        diff = None

        parameters = []
        if prevLayer:
            # Place prev layer on current layer's canvas
            parameters = projectPrevLayerParametersToCurrent(prevLayerConfig, layerConfig)
            referenceImg = projectPrevLayerToCurrent(prevLayer, *parameters)

            # Create a diff image
            diff = diffImage(targetImg, referenceImg)
        return targetImg, parameters, diff

    layers = []
    prevLayer = None
    prevLayerConfig = None
    for layerConf in config:
        layerConfig = LayerConfig(img, layerConf)
        prevLayer, parameters, diff = createLayer(img, layerConfig, prevLayer, prevLayerConfig)
        prevLayerConfig = layerConfig
        layers.append((diff or prevLayer, parameters, layerConfig.img_width))

    return layers

