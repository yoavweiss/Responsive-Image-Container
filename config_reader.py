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
    { 'crop': (0, 0, 600, 400),
      'position': (200, 0),
      'rotate': 90} ]
"""

class LayerConfig(object):
    def __init__(self, img, config):
        width, height = img.size
        ratio = float(height) / width
        self.crop = tuple(config.get('crop', [0, 0, width, height]))
        self.img_width = config.get('imgwidth', codec_utils.cropDimensions(self.crop)[0])
        self.position = tuple(config.get('position', [0,0]))
        canvasWidth = self.img_width + self.position[0]
        self.canvas_dimensions = (canvasWidth, int(canvasWidth*ratio))
        self.rotate = float(config.get('rotate', 0))

