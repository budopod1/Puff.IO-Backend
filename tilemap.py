from math import floor, ceil
from biomes import Biome
from tiles import TILE_TYPES


class Tilemap:
  def __init__(self):
    self.tiles = {}
    self.biome = Biome()
  
  def render(self):
    images = []
    for pos, tile in self.tiles.items():
      if tile:
        images.append(tile.render(*pos))
    return images
  
  def generate(self, x, y):
    return self.biome.generate(x, y)

  def set(self, tile, x, y):
    self.tiles[(x, y)] = tile

  def get(self, x, y):
    if (x, y) not in self.tiles:
      tile = self.generate(x, y)
      self.set(tile, x, y)
      return tile
    return self.tiles[(x, y)]
  
  def save(self):
    return [
      {
        "position": list(position),
        "type": type(tile).__name__,
        "data": tile.save()
      }
      for position, tile in self.tiles.copy().items()
      if tile
    ]
  
  def view(self, x, y, xd, yd):
    for vx in range(floor(x - xd), ceil(x + xd + 1)):
      for vy in range(floor(y - yd), ceil(y + yd + 1)):
        self.get(vx, vy)
  
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
