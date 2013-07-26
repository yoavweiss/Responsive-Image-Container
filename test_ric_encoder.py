#!/usr/bin/python

import unittest
from PIL import Image
from ric_encoder import ric_encode

class TestRicEncoder(unittest.TestCase):
    def testEncoder(self):
        img = Image.open("samples/obama.jpg")
        options = {"resolutions":[300, 500, 1000]}
        output = ric_encode(img, "res_switch", options)
        f = open("/tmp/test.ric", "wb")
        f.write(output)
        f.close()



def main():
    unittest.main()

if __name__ == '__main__':
    main()
