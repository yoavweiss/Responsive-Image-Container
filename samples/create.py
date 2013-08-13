#!/usr/bin/python

from PIL import Image

org=Image.open("obama.jpg")
org.save("/tmp/obama.png", "PNG")
small=org.copy()
ret = small.crop((210, 120, 510, 420))
ret.save("/tmp/small.png", "PNG")
med=org.copy()
med=med.crop((180, 70, 720, 480))
med.save("/tmp/med.png", "PNG")

