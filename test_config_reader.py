#!/usr/bin/python

import unittest
from config_reader import LayerConfig
from PIL import Image

class TestConfigReader(unittest.TestCase):
    def testEmptyConfig(self):
        img = Image.new('RGB', (100, 100), '#50D0FF')
        conf = LayerConfig(img, {})
        self.assertEqual(conf.img_width, 100)
        
	

         
def main():
    unittest.main()

if __name__ == '__main__':
    main()
