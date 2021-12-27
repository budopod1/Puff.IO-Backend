from image import Image


class Tilemap:
  def __init__(self):
    self.tiles = {}
  
  def render(self):
    images = []
    for pos, tile in self.tiles.items():
      images.append(tile.render(*pos))
    return images
  
  def set(self, tile, x, y):
    self.tiles[(x, y)] = tile

  def get(self, x, y):
    if (x, y) not in self.tiles:
      return None
    return self.tiles[(x, y)]
  
  def save(self):
    return [
      {
        "position": list(position),
        "type": type(tile).__name__,
        "data": tile.save()
      }
      for position, tile in self.tiles.items()
    ]
  
  @classmethod
  def load(cls, data):
    tilemap = cls()
    for tile in data:
      tile_class = None
      for tile_type in TILE_TYPES:
        if tile["type"] == tile_type.__name__:
          tile_class = tile_type
      tilemap.set(tile_class.load(tile["data"]), *tile["position"])
    return tilemap


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
