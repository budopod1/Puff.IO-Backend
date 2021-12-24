class Camera:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.size = 7
  
  def render(self):
    return {"x": self.x, "y": self.y, "size": self.size}
  
  def save(self):
    return self.render()
  
  @classmethod
  def load(cls, data):
    camera = cls()
    camera.x = data["x"]
    camera.y = data["y"]
    camera.size = data["size"]
    return camera
