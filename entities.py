from image import Image


class Entity:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.xv = 0
    self.yv = 0
    self.xg = 0
    self.yg = -1
    self.grounded_x = False
    self.grounded_y = False
    self.active = True
    self.sprite = Image("error")
    self.collide_points = [(0, 0)]
  
  def frame(self):
    if self.active:
      self.grounded_x = False
      self.grounded_y = False

      self.xv += self.xg * time_delta
      self.yv += self.yg * time_delta

      x_change = self.xv * time_delta
      self.x += x_change
      if self.collides(self.x, self.y):
        self.x -= x_change
        self.xv = 0
        self.grounded_x = True
      
      y_change = self.yv * time_delta
      self.y += y_change
      if self.collides(self.x, self.y):
        self.y -= y_change
        self.yv = 0
        self.grounded_y = True
  
  def collides(self, x, y):
    tiles = []
    for point in self.collide_points:
      tile = tilemap.get(round(x + point[0]), round(y + point[1]))
      if tile:
        tiles.append(tile)
    return tiles
  
  def render(self):
    return self.sprite.render(self.x, self.y)
  
  def __repr__(self):
    return f"{type(self).__name__} @ ({self.x}, {self.y})" 


class Player(Entity):
  def __init__(self, x, y, user):
    super().__init__(x, y)
    self.user = user
    self.username = user.username
    self.sprite = Image("puff")
    self.jump_power = 2.5
    self.collide_points = [
      (-0.5, 0.05),
      (0.5, 0.05),
      (-0.5, -0.05),
      (0.5, -0.05),
      (-0.3535, -0.3535),
      (-0.3535, 0.3535),
      (0.3535, 0.3535),
      (0.3535, -0.3535),
      (0.05, -0.5),
      (-0.05, -0.5),
      (0.05, 0.5),
      (-0.05, 0.5)
    ]

  def frame(self):
    super().frame()
    self.active = users[self.username].is_active
    if self.active:
      if "KeyW" in users[self.username].get_just_down():
        self.yv += self.jump_power
