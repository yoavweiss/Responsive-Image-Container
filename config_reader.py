import codec_utils
"""
{
# canvaswidth - the final layer's dimension width
# imgwidth - The image data dimensions on the final layer
# crop - The final layer's crop from the original image
# position - The image's position on the canvas
# rotate - The image's rotate on the canvas
# Example:
  [ { 'img_width': 200,
      'crop': (0, 0, 300, 300)},
    { 'crop': (0, 0, 600, 400) } ]
"""

class LayerConfig(object):
    def __init__(self, img, config):
        width, height = img.size
        self.crop = tuple(config.get('crop', [0, 0, width, height]))
        cropWidth, cropHeight = codec_utils.cropDimensions(self.crop)
        cropRatio = float(cropHeight) / cropWidth
        self.imgWidth = config.get('imgwidth', cropWidth)
        self.imgHeight = int(self.imgWidth * cropRatio)

