from time import perf_counter
from server import Server
from user import User


class State:
  def __init__(self):
    # Manage the global state off the whole MMO
    self.time_delta = 0
    self.last_tick = 0
    self.users = {}
    self.servers = []
  
  def add_server(self, server):
    self.servers.append(server)
  
  def tick(self):
    self.time_delta = perf_counter() - self.last_tick
    self.last_tick = perf_counter()
  
  def save(self):
    return {
      "servers": [server.save() for server in self.servers],
      "users": {username: user.save() for username, user in self.users.items()}
    }
  
  @classmethod
  def load(cls, data):
    state = cls()
    for server in data["servers"]:
      state.add_server(Server.load(state, server))
    for username, user in data["users"].items():
      state.users[username] = User.load(state, user)
