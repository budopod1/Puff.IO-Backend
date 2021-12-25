from uuid import uuid4 as uuid
from tiles import Tilemap
from entities import ENTITY_TYPES


class Server:
  def __init__(self, state):
    # Manage a single server
    self.uuid = str(uuid())
    self.state = state
    self.tilemap = None
    self.background = "#000000"
    self.images = []
    self.entities = []
  
  def set_tilemap(self, tilemap):
    self.tilemap = tilemap
  
  def tick(self):
    self.images = []
    self.background = "#000000"

  def render(self):
    return {"background": self.background, "images": self.images}
  
  def save(self):
    return {
      "uuid": self.uuid,
      "tilemap": self.tilemap.save(),
      "entities": [
        entity.save()
        for entity in self.entities
      ]
    }
  
  @classmethod
  def load(cls, state, data):
    server = cls(state)
    server.uuid = data["uuid"]
    server.tilemap = Tilemap.load(data["tilemap"])
    for entity in data["entities"]:
      entity_class = None
      for entity_type in ENTITY_TYPES:
        if entity_type.__name__ == entity["type"]:
          entity_class = entity_type
      server.entities.append(entity_class.load(state, entity))
    return server
