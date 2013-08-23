from PIL import Image
import iso_media

from codec_utils import diffImage, projectPrevLayerToCurrent, cropDimensions, gcd
from config_reader import LayerConfig

class Coder(object):

    def createTargetImage(self, img, parameter):
        target = img.copy()
        # crop the target image from the original image
        target=target.crop(parameter.crop)

        # resize it to match the width
        target.thumbnail((parameter.imgWidth, parameter.imgWidth), Image.ANTIALIAS)

        return target

    def imgProportion(self, crop):
        width, height = cropDimensions(crop)
        return float(height) / width

    def projectPrevLayerParametersToCurrent(self, prevLayerConfig, currLayerConfig):

        # find current layer crop width divided by prev layer's crop width,
        # to get the dimensions to which we need to inflate the previous layer
        currWidth = cropDimensions(currLayerConfig.crop)[0]
        prevWidth, prevHeight = cropDimensions(prevLayerConfig.crop)
        numerator = prevWidth * currLayerConfig.imgWidth
        denominator = currWidth * prevLayerConfig.imgWidth
        divisor = gcd(numerator, denominator)
        ratio = (numerator / divisor, denominator / divisor)

        currResizeRatio = (float(currWidth)/currLayerConfig.imgWidth)

        # Find the lower layer's position on the upper layer, to inverse the crop
        currCropX0, currCropY0, currCropX1, currCropY1 = currLayerConfig.crop
        prevCropX0, prevCropY0, prevCropX1, prevCropY1 = prevLayerConfig.crop
        position = (int(float(prevCropX0 - currCropX0)/currResizeRatio), 
                    int(float(prevCropY0 - currCropY0)/currResizeRatio))
        canvasDimensions = (currLayerConfig.imgWidth, currLayerConfig.imgHeight)
        return canvasDimensions, position, ratio

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
            layers.append((diff or prevLayer, parameters, layerConfig.imgWidth))

        return layers

