#!/usr/bin/python

import unittest

import iso_media

class IsoMediaTests(unittest.TestCase):

    def testRead(self):
        data1 = "\x00\x00\x00\x0bftypbla"
        length, type, payload = iso_media.read_box(data1)
        self.failUnless(length == 11)
        self.failUnless(type == "ftyp")
        self.failUnless(payload == "bla")
        
    def testWrite(self):
        data1 = "\x00\x00\x00\x0bftypbla"
        output = iso_media.write_box("ftyp", "bla")
        self.failUnless(output == data1)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
