from PIL import Image, ImageChops
from algo import Algo

class ResSwitchEncoder(Algo.Encoder):

    def createLayer(self, referenceImg, width):
        img = self.orgImg.copy()
        diff = None
        img.thumbnail((width, width), Image.ANTIALIAS)
        print "ImgLayer", img, self.orgImg
        if referenceImg:
            upscaledReference = referenceImg.resize(img.size, Image.ANTIALIAS)
            diff = ImageChops.subtract(img, upscaledReference)
        return img, diff

    def readOptions(self):
        self.resolutions = self.options['resolutions']

    def encode(self):
        self.readOptions()
        layers = []
        prevLayer = None
        for res in self.resolutions:
            currLayer, diff = self.createLayer(prevLayer, res)
            if diff:
                layers.append(diff)
            else:
                layers.append(currLayer)
            prevLayer = currLayer
        return layers

class ResSwitchDecoder(Algo.Decoder):
    def decode(self):
        img = None
        for layer in self.layers:
            if not img:
                img = layer
                continue
            upscaled = img.resize(layer.size, Image.ANTIALIAS)
            img = ImageChops.add(upscaled, layer)
        return img



