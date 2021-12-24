from uuid import uuid4 as uuid


class Server:
  def __init__(self, state):
    # Manage a single server
    self.uuid = uuid()
    self.state = state
    self.tilemap = None
    self.background = "black"
    self.images = []
    self.entities = []
  
  def set_tilemap(self, tilemap):
    self.tilemap = tilemap
  
  def tick(self):
    self.images = []
    self.background = "black"

  def render(self):
    return {"background": self.background, "images": self.images}
