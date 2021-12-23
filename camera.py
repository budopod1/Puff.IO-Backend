class Camera:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.size = 7
  
  def render(self):
    return {"x": self.x, "y": self.y, "size": self.size}
