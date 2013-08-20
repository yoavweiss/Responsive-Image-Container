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
            layer[0].save(layerFileName, "WEBP", quality=90)
            #layer[0].save(layerFileName+".png", "PNG", quality=95)
            # TODO: Run ssim test to see that the image we got is correct
            layer2 = Image.open(layerFileName)
            layers2.append(layer2)
        #decoder = res_switch.ResSwitch.Algo.Decoder(layers2)
        #dcd = decoder.decode()
        #dcd.save("/tmp/decoded.png", "PNG")
        #img.save("/tmp/crop.png", "PNG")

    def testEncodeCrop(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        self.encode("samples/crop.jpg", "samples/crop_config.txt")

    def testEncodeResSwitch(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        self.encode("samples/res_switch.png", "samples/res_switch_config.txt")

    def testCreateTargetImage(self):
        img = Image.open("samples/crop.jpg")
        encoder = coder.Coder()
        # Create a crop and resize it
        layerConf = LayerConfig(img, {"imgwidth": 200, "crop":(0, 0, 300, 300)})
        target = encoder.createTargetImage(img, layerConf)
        target.save("/tmp/target1.webp", "WEBP", quality=95)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
