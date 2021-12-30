class Camera:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.size = 7
  
  def render(self):
    return {"x": self.x, "y": self.y, "size": self.size}
  
  def proccess(self, data):
    background = data["background"]
    images = data["images"]
    new_images = []
    for image in images:
      if abs(image["x"] - self.x) < self.size + image["size"]:
        if abs(image["y"] - self.y) < self.size / 2 + image["size"]:
          new_images.append(image)
    return {"background": background, "images": new_images}
  
  def save(self):
    return self.render()
  
  @classmethod
  def load(cls, data):
    camera = cls()
    camera.x = data["x"]
    camera.y = data["y"]
    camera.size = data["size"]
    return camera
