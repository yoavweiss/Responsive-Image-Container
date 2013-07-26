#!/usr/bin/python

import unittest
import res_switch
import PIL

class TestResSwitchAlgo(unittest.TestCase):

    def testCreateLayers(self):
        # Currently this test passes anyway, but it creates a bunch of file that enable to peek into the outputs
        # Improvements: ssim test, output layers file size and final output file size
        img = PIL.Image.open("samples/obama.jpg")
        encoder = res_switch.ResSwitch.Algo.Encoder(img, {"resolutions":[300, 500, 1000]})
        layers = encoder.encode()
        i = 0
        layers2 = []
        for layer, res in layers:
            i += 1
            layerFileName = "/tmp/layer" + str(i) + ".webp"
            if i == 1:
                layer.save(layerFileName, "WEBP", quality=95)
            else:
                layer.save(layerFileName, "WEBP", quality=95)
            # TODO: Run ssim test to see that the image we got is correct
            layer2 = PIL.Image.open(layerFileName)
            layers2.append(layer2)
        decoder = res_switch.ResSwitch.Algo.Decoder(layers2)
        dcd = decoder.decode()
        dcd.save("/tmp/decoded.png", "PNG")
        img.save("/tmp/obama.png", "PNG")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
