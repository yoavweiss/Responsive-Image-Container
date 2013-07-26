
class Algo:
    
    @classmethod
    def getPixels(self, img):
        img.convert('RGB')
        return list(img.getdata())
    class Encoder:
        def __init__(self, orgImg, options):
            self.orgImg = orgImg
            self.options = options

        def encode(self):
            print >> sys.stderr, "Encode shouldn't be called from base Algo.Encoder"

    class Decoder:
        def __init__(self, layers):
            self.layers = layers

        def decode(self):
            print >> sys.stderr, "Decode shouldn't be called from base Algo.Decoder"


