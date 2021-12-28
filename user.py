import bcrypt
from time import time
from camera import Camera


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt()).decode("UTF-8")

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password.encode("UTF-8"))


class User:
  def __init__(self, state, username, password):
    self.state = state
    self.username = username
    self.password = get_hashed_password(password)
    self.last_tick = 0
    self.is_active = False
    self.keys_down = {}
    self.just_down = []
    self.camera = Camera()
    self.server = None
    self.server_uuid = None
  
  def change_server(self, server):
    self.server = server
  
  def frame(self):
    self.is_active = self.last_tick > time() - 1
  
  def update(self, message):
    self.last_tick = time()
    self.keys_down = message["keys_down"]
    self.just_down += message["just_down"]
  
  def check(self, password):
    return check_password(password, self.password)
  
  def is_key_down(self, key):
    return key in self.keys_down
  
  def get_just_down(self):
    self.just_down, jd = [], self.just_down
    return jd
  
  def save(self):
    return {
      "server": self.server.uuid,
      "camera": self.camera.save(),
      "username": self.username,
      "password": self.password
    }
  
  @classmethod
  def load(cls, state, data):
    user = cls(state, data["username"], b"this is insucure!")
    user.password = data["password"]
    user.camera = Camera.load(data["camera"])
    user.server_uuid = data["server"]
    return user
  
  def load_server(self):
    self.server = self.state.get_server(self.server_uuid)
