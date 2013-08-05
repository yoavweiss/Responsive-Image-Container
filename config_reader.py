"""
{
# canvaswidth - the final layer's dimension width
# imgwidth - The image data dimensions on the final layer
# crop - The final layer's crop from the original image
# position - The image's position on the canvas
# rotate - The image's rotate on the canvas
# Example:
  [ { 'canvaswidth': 300, 
      'imgwidth': 300,
      'crop': (0, 0, 300, 300)},
    { 'canvaswidth': 600,
      'imgwidth': 800,
      'crop': (0, 0, 600, 400),
      'position': (200, 0),
      'rotate': 90} ]
"""

class LayerConfig(object):
    def __init__(self, img, config):
        width, height = img.size
        ratio = float(height) / width
        canvasWidth = int(config.get('canvaswidth', width))
        self.canvas_dimensions = (canvasWidth, int(canvasWidth*ratio))
        self.img_width = int(config.get('imgwidth', width))
        self.crop = tuple(config.get('crop', [0, 0, width, height]))
        self.position = tuple(config.get('position', [0,0]))
        self.rotate = float(config.get('rotate', 0))

