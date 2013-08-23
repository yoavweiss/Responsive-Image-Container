from PIL import Image
from codec_utils import undiffImage, projectPrevLayerToCurrent

class Decoder(object):
    def rebuildImage(self, prevLayer, currLayer, parameters):
        base = projectPrevLayerToCurrent(prevLayer, *parameters)
        return undiffImage(currLayer, base)

    def decode(self, layers):
        img = None
        for layer, parameters in layers:
            if not img:
                img = layer
                continue
            img = self.rebuildImage(img, layer, parameters)
        return img
