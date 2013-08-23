#!/usr/bin/python

import unittest
from PIL import Image
from ric_encoder import ric_encode, ric_decode

class TestRicEncoder(unittest.TestCase):
    def testEncoder(self):
        img = open("samples/crop.jpg","rb").read()
        options = [ { "imgwidth": 200, "crop": [210, 120, 510, 420]}, { "imgwidth": 400, "crop": [180, 90, 720, 480] } ]
        output = ric_encode(img, options)
        f = open("/tmp/test.ric", "wb")
        f.write(output)
        f.close()

    def testDecoder(self):
        img = open("/tmp/test.ric","rb").read()
        output = ric_decode(img)
        f = open("/tmp/test.webp", "wb")
        f.write(output)
        f.close()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
