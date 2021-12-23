from image import Image


class Tilemap:
  def __init__(self, server):
    self.server = server
    self.tiles = {}
  
  def render(self):
    for pos, tile in self.tiles.items():
      self.server.images.append(tile.render(*pos))
  
  def set(self, tile, x, y):
    self.tiles[(x, y)] = tile

  def get(self, x, y):
    if (x, y) not in self.tiles:
      return None
    return self.tiles[(x, y)]


class Tile:
  def __init__(self):
    self.sprite = Image("error")
  
  def render(self, x, y):
    return self.sprite.render(x, y)


class Grass(Tile):
  def __init__(self):
    self.sprite = Image("grass")