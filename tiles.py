from image import Image


class Tile:
  def __init__(self):
    self.sprite = Image("error")
  
  def render(self, x, y):
    return self.sprite.render(x, y)
  
  def save(self):
    return {}
  
  @classmethod
  def load(cls, data):
    return cls()


class Grass(Tile):
  def __init__(self):
    self.sprite = Image("grass")


TILE_TYPES = [Tile, Grass]
