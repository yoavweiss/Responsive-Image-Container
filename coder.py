from PIL import Image
import algo
import iso_media

from codec_utils import diffImage, projectPrevLayerToCurrent, cropDimensions
from config_reader import LayerConfig


class Coder(object):

    def createTargetImage(self, img, parameter):
        target = img.copy()
        # crop the target image from the original image
        target=target.crop(parameter.crop)

        # resize it to match the width
        target.thumbnail((parameter.img_width, parameter.img_width), Image.ANTIALIAS)

        # rotate
        target=target.rotate(parameter.rotate)

        # position it on the canvas
        width, height = target.size
        posX, posY = parameter.position
        output = Image.new('RGBA', parameter.canvas_dimensions, (0, 0, 0, 0))
        output.paste(target, (posX, posY))
        return output

    def imgProportion(self, crop):
        width, height = cropDimensions(crop)
        return float(height) / width

    def projectPrevLayerParametersToCurrent(self, prevLayerConfig, currLayerConfig):
        # Calculate the previous layer's crop, to compensate for offset
        posX, posY = prevLayerConfig.position
        imgWidth = prevLayerConfig.img_width
        imgHeight = int(imgWidth * self.imgProportion(prevLayerConfig.crop))
        crop = (posX, posY, posX + imgWidth, posY + imgHeight)

        # calculate the rotate angle difference
        rotateAngle = prevLayerConfig.rotate - currLayerConfig.rotate
        if rotateAngle < 0:
            rotateAngle += 360

        # find current layer crop width divided by prev layer's crop width,
        # to get the dimensions to which we need to inflate the previous layer
        currWidth = cropDimensions(currLayerConfig.crop)[0]
        prevWidth, prevHeight = cropDimensions(prevLayerConfig.crop)
        prevResizeRatio = (float(prevWidth)/prevLayerConfig.img_width)
        currResizeRatio = (float(currWidth)/currLayerConfig.img_width)
        ratio = prevResizeRatio/currResizeRatio
        prevWidth = float(prevWidth)/prevResizeRatio
        prevHeight = float(prevHeight)/prevResizeRatio
        projectionSize = (int(prevWidth*ratio), int(prevHeight*ratio))

        # Find the lower layer's position on the upper layer, to inverse the crop
        currCropX0, currCropY0, currCropX1, currCropY1 = currLayerConfig.crop
        prevCropX0, prevCropY0, prevCropX1, prevCropY1 = prevLayerConfig.crop
        position = (int(float(prevCropX0 - currCropX0)/currResizeRatio), 
                    int(float(prevCropY0 - currCropY0)/currResizeRatio))
        return currLayerConfig.canvas_dimensions, position, projectionSize, rotateAngle, crop

    def createLayer(self, img, layerConfig, prevLayer, prevLayerConfig):
        targetImg = self.createTargetImage(img, layerConfig)
        diff = None

        parameters = []
        if prevLayer:
            # Place prev layer on current layer's canvas
            parameters = self.projectPrevLayerParametersToCurrent(prevLayerConfig, layerConfig)
            referenceImg = projectPrevLayerToCurrent(prevLayer, *parameters)

            # Create a diff image
            diff = diffImage(targetImg, referenceImg)
        return targetImg, parameters, diff

    def encode(self, img, config):
        if not len(config):
            return
        layers = []
        prevLayer = None
        prevLayerConfig = None
        config.append({})
        for layerConf in config:
            layerConfig = LayerConfig(img, layerConf)
            prevLayer, parameters, diff = self.createLayer(img, layerConfig, prevLayer, prevLayerConfig)
            prevLayerConfig = layerConfig
            layers.append((diff or prevLayer, parameters, layerConfig.img_width))

        return layers

