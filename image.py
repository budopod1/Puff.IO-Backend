class Image:
  def __init__(self, sprite):
    self.sprite = sprite
    self.size = 1
  
  def render(self, x, y):
    return {"sprite": self.sprite, "x": x, "y": y, "size": self.size}
  
  def save(self):
    data = self.render(0, 0)
    del data["x"]
    del data["y"]
    return data
  
  @classmethod
  def load(cls, data):
    image = cls(data["sprite"])
    image.size = data["size"]
    return image
