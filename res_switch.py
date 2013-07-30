from PIL import Image
import algo
from StringIO import StringIO
import iso_media

class ResSwitch(object):
    class Algo(algo.Algo):
        class Encoder(algo.Algo.Encoder):

            def createLayer(self, referenceImg, width):
                img = self.orgImg.copy()
                diff = None
                img.thumbnail((width, width), Image.ANTIALIAS)
                if referenceImg:
                    upscaledReference = referenceImg.resize(img.size, Image.ANTIALIAS)
                    diff = self.diffImage(img, upscaledReference)
                return img, diff

            def diffImage(self, highQ, lowQ):
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

            def encode(self):
                self.resolutions = self.options['resolutions']
                layers = []
                prevLayer = None
                for res in self.resolutions:
                    currLayer, diff = self.createLayer(prevLayer, res)
                    if diff:
                        layers.append((diff, res))
                    else:
                        layers.append((currLayer, res))
                    prevLayer = currLayer
                return layers

        class Decoder(algo.Algo.Decoder):
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
                diffPixels = ResSwitch.Algo.getPixels(diff)
                lowQPixels = ResSwitch.Algo.getPixels(lowQ)
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

    class Wrapper(object):
        def writeImageBuffer(self, layer, quality):
            output = StringIO()
            layer.save(output, "WEBP", quality=quality)
            buf = output.getvalue()
            output.close()
            return buf

        def readImageBuffer(self, buf):
            io = StringIO(buf)
            img = Image.open(io)
            io.close()
            return img

        def wrapLayer(self, layer, first, quality):
            type = "LAHD"
            if first:
                type = "LBAS"

            return iso_media.write_box(type, self.writeImageBuffer(layer, quality))

        def wrapLayers(self, layers, quality = 95, diffquality = 90):
            first = True
            buf = ""
            offset = 0
            offsetTable = []
            for layer, res in layers:
                currLayer = self.wrapLayer(layer, first, quality)
                offsetTable.append((offset + len(currLayer), res))

                buf += currLayer
                first = False
                quality = diffquality
            return buf, offsetTable

        def unwrapLayers(self, buf):
            bufLen = len(buf)
            offset = 0
            layers = []
            while offset < bufLen:
                boxLen, boxType, payload = iso_media.read_box(buf[offset:])
                offset += boxLen
                layers.append(self.readImageBuffer(payload))

            return layers

