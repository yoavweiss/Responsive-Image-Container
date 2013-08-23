from StringIO import StringIO
from PIL import Image
import iso_media

params_num = {  "LBAS": 0,
                "LAEN": 3 }
def wrapLayers(layers, quality = 95, diffquality = 90):
    def wrapLayer(layer, boxtype, quality, parameters):
        def writeImageBuffer():
            buf = ""
            for param in parameters:
                for val in param:
                    buf += iso_media.write_int16(val)
            output = StringIO()
            layer.save(output, "WEBP", quality=quality)
            buf += output.getvalue()
            output.close()
            return buf

        return iso_media.write_box(boxtype, writeImageBuffer())

    first = True
    buf = ""
    offset = 0
    offsetTable = []
    for layer, parameters, res in layers:
        currLayer = wrapLayer(  layer, 
                                "LBAS" if first else "LAEN",
                                quality if first else diffquality,
                                parameters)
        offsetTable.append((offset + len(currLayer), res))

        buf += currLayer
        first = False
    return buf, offsetTable

def unwrapLayers(buf):
    def readImageBuffer(imgbuf, type):
        offset = 0
        parameters = []
        for i in range(params_num[type]):
            parameters.append((iso_media.read_int16(imgbuf[offset:]),
                               iso_media.read_int16(imgbuf[offset+2:])))
            offset += 4



        io = StringIO(imgbuf[offset:])
        img = Image.open(io)
        io.close()
        return img, parameters
    bufLen = len(buf)
    offset = 0
    layers = []
    while offset < bufLen:
        boxLen, boxType, payload = iso_media.read_box(buf[offset:])
        offset += boxLen
        layers.append(readImageBuffer(payload, boxType))

    return layers
