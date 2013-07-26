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
            diff = self.diffImage(img, upscaledReference)
        return img, diff

    def diffImage(self, highQ, lowQ):
        highQPixels = Algo.getPixels(highQ)
        lowQPixels = Algo.getPixels(lowQ)
        diffPixels = []
        for h, l in zip(highQPixels, lowQPixels):
            pixel = []
            for i in range(3):
                pixel.append((h[i] - l[i] + 256) / 2)
            diffPixels.append(tuple(pixel))
        diff = Image.new("RGB", highQ.size)
        diff.putdata(diffPixels)
        return diff

    def encode(self):
        self.resolutions = self.options['resolutions']
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
            img = self.rebuildImage(layer, upscaled)
        return img

    def rebuildImage(self, diff, lowQ):
        diffPixels = Algo.getPixels(diff)
        lowQPixels = Algo.getPixels(lowQ)
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



