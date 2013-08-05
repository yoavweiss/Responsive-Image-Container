from PIL import Image
from codec_utils import undiffImage

def decode(layers):
    img = None
    for layer in layers:
        if not img:
            img = layer
            continue
        upscaled = img.resize(layer.size, Image.ANTIALIAS)
        img = rebuildImage(layer, upscaled)
    return img
