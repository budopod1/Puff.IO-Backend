import bcrypt
from time import time
from camera import Camera


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


class User:
  def __init__(self, username, password):
    self.username = username
    self.password = get_hashed_password(password)
    self.last_tick = time()
    self.is_active = True
    self.keys_down = {}
    self.just_down = []
    self.camera = Camera()
    self.server = None
  
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
