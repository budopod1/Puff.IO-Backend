class Image:
  def __init__(self, sprite):
    self.sprite = sprite
    self.size = 1
  
  def render(self, x, y):
    return {"sprite": self.sprite, "x": x, "y": y, "size": self.size}