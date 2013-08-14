#!/usr/bin/python

import unittest
import coder
from PIL import Image
import json
from config_reader import LayerConfig

class TestCoder(unittest.TestCase):

    def encode(self, filename, configname):
        img = Image.open(filename)
        basename=filename.split("/")[1]
        config = json.load(open(configname, "rb"))
        layers = coder.Coder().encode(img, config)
        i = 0
        layers2 = []
        for layer in layers:
            i += 1
            layerFileName = "/tmp/" + basename + "_layer" + str(i) + ".webp"
            layer[0].save(layerFileName, "WEBP", quality=95)
            layer[0].save(layerFileName+".png", "PNG", quality=95)
            # TODO: Run ssim test to see that the image we got is correct
            layer2 = Image.open(layerFileName)
            layers2.append(layer2)
        #decoder = res_switch.ResSwitch.Algo.Decoder(layers2)
        #dcd = decoder.decode()
        #dcd.save("/tmp/decoded.png", "PNG")
        #img.save("/tmp/obama.png", "PNG")

    def testEncodeCrop(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        self.encode("samples/obama.jpg", "samples/obama_config.txt")

    def testEncodeRotate(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        self.encode("samples/iphone.png", "samples/iphone_config.txt")

    def testCreateTargetImage(self):
        img = Image.open("samples/obama.jpg")
        encoder = coder.Coder()
        # Create a crop and rotate it
        layerConf = LayerConfig(img, {"crop":(0, 0, 300, 300), "rotate": 90})
        target = encoder.createTargetImage(img, layerConf)
        target.save("/tmp/target1.webp", "WEBP", quality=95)
        # Create a crop rotate and resize it
        layerConf = LayerConfig(img, {"imgwidth": 200, "crop":(0, 0, 300, 300), "rotate": 90})
        target = encoder.createTargetImage(img, layerConf)
        target.save("/tmp/target2.webp", "WEBP", quality=95)
        # Create a crop, rotate, resize it and reposition
        layerConf = LayerConfig(img, {"imgwidth": 200, "canvaswidth": 400, "crop":(0, 0, 300, 300), "rotate": 90, "position":(200, 0)})
        target = encoder.createTargetImage(img, layerConf)
        target.save("/tmp/target3.webp", "WEBP", quality=95)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
