#!/usr/bin/python

import unittest
import coder
from PIL import Image
import json

class TestCoder(unittest.TestCase):

    def testEncode(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        img = Image.open("samples/obama.jpg")
        config = json.load(open("config.txt", "rb"))
        layers = coder.encode(img, config)
        i = 0
        layers2 = []
        for layer in layers:
            i += 1
            layerFileName = "/tmp/layer" + str(i) + ".webp"
            if i == 1:
                layer[0].save(layerFileName, "WEBP", quality=95)
            else:
                layer[0].save(layerFileName, "WEBP", quality=95)
            # TODO: Run ssim test to see that the image we got is correct
            layer2 = Image.open(layerFileName)
            layers2.append(layer2)
        #decoder = res_switch.ResSwitch.Algo.Decoder(layers2)
        #dcd = decoder.decode()
        #dcd.save("/tmp/decoded.png", "PNG")
        #img.save("/tmp/obama.png", "PNG")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
