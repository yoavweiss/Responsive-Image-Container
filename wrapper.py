from StringIO import StringIO
from PIL import Image
import iso_media

PARAM_NUM = 5

def wrapLayers(layers, quality = 95, diffquality = 90):
    def wrapLayer(layer, boxtype, quality, parameters):
        def writeImageBuffer():
            def writeValue(val):
                if type(val) is float:
                    val = int(val*100)
                return iso_media.write_int16(val)
            assert not parameters or len(parameters) == PARAM_NUM, "Wrong parameters number. Decoder won't be able to decode this"
            buf = ""
            for param in parameters:
                if type(param) is tuple:
                    for val in param:
                        buf += writeValue(val)
                else:
                    buf += writeValue(param)
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
    print layers
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
    def readImageBuffer(imgbuf):
        offset = 0
        parameters = []
        for i in range(PARAM_NUM):
            parameters.append(iso_media.read_int32(imgbuf[offset]))
            offset += 4


        io = StringIO(imgbuf[PARAM_NUM*4:])
        img = Image.open(io)
        io.close()
        return img, parameters
    bufLen = len(buf)
    offset = 0
    layers = []
    while offset < bufLen:
        boxLen, boxType, payload = iso_media.read_box(buf[offset:])
        offset += boxLen
        layers.append(readImageBuffer(payload))

    return layers
