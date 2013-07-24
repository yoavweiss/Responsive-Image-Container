#!/usr/bin/python

import unittest
import res_switch
import PIL

class TestResSwitchAlgo(unittest.TestCase):

    def testCreateLayers(self):
        img = PIL.Image.open("samples/obama.jpeg")
        encoder = res_switch.ResSwitchEncoder(img, {"resolutions":[300, 500, 1000]})
        layers = encoder.encode()
        i = 0
        for layer in layers:
            i += 1
            layer.save("/tmp/layer" + str(i) + ".jpg", "JPEG")
            # TODO: Run ssim test to see that the image we got is correct
        decoder = res_switch.ResSwitchDecoder(layers)
        dcd = decoder.decode()
        dcd.save("/tmp/decoded.jpg", "JPEG")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
