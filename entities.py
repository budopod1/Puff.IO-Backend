from image import Image


class Entity:
  def __init__(self, server, state, x, y):
    self.server = server
    self.state = state
    self.x = x
    self.y = y
    self.xv = 0
    self.yv = 0
    self.xg = 0
    self.yg = -2.5
    self.grounded_x = False
    self.grounded_y = False
    self.active = True
    self.sprite = Image("error")
    self.collide_points = [(0, 0)]
  
  def frame(self):
    if self.active:
      self.grounded_x = False
      self.grounded_y = False

      self.xv += self.xg * self.state.time_delta
      self.yv += self.yg * self.state.time_delta

      x_change = self.xv * self.state.time_delta
      self.x += x_change
      if self.collides(self.x, self.y):
        self.x -= x_change
        self.xv = 0
        self.grounded_x = True
      
      y_change = self.yv * self.state.time_delta
      self.y += y_change
      if self.collides(self.x, self.y):
        self.y -= y_change
        self.yv = 0
        self.grounded_y = True
  
  def collides(self, x, y):
    tilemap = self.state.get_server(self.server).tilemap
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
  
  def __str__(self):
    return self.__repr__()
  
  def save(self):
    return {
      "xv": self.xv,
      "yv": self.yv,
      "x": self.x,
      "y": self.y,
      "type": type(self).__name__,
      "active": self.active,
      "sprite": self.sprite.save(),
      "server": self.server
    }
  
  @classmethod
  def load(cls, state, data):
    entity = cls(data["server"], state, data["x"], data["y"])
    entity.active = data["active"]
    entity.sprite = Image.load(data["sprite"])
    entity.xv = data["xv"]
    entity.yv = data["yv"]

    return entity


class Player(Entity):
  def __init__(self, server, state, x, y, user=None):
    super().__init__(server, state, x, y)
    self.active = False
    self.user = user
    self.username = user.username if user else None
    self.sprite = Image("puff")
    self.jump_power = 3.5
    self.move_power = 1
    self.ground_power = 2
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
    self.active = self.user.is_active and self.user.server.uuid == self.server
    super().frame()
    if self.active:
      if self.user.is_key_down("KeyW") and self.grounded_y:
        self.yv += self.jump_power
      
      move_speed = self.move_power * self.state.time_delta
      if self.ground_power:
        move_speed *= self.ground_power

      if self.user.is_key_down("KeyD"):
        self.xv += move_speed
      
      if self.user.is_key_down("KeyA"):
        self.xv -= move_speed
      
      if self.user.is_key_down("KeyS"):
        self.xv = 0
        self.yv = -5
      
      self.user.camera.x = self.x
      self.user.camera.y = self.y

      camera_size = self.user.camera.size
      self.server.tilemap.view(self.x, self.y, camera_size, camera_size * 3)
  
  def save(self):
    entity = super().save()

    entity.update({
      "username": self.user.username
    })

    return entity
  
  @classmethod
  def load(cls, state, data):
    entity = super().load(state, data)

    entity.username = data["username"]
    entity.user = state.users[data["username"]]

    return entity


ENTITY_TYPES = [Player, Entity]
