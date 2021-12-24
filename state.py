from time import perf_counter


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
