from replit import db
from state import State
from server import Server
from tiles import Tilemap, Grass


def load_state():
  try:
    if not db["setup"]:
      raise Exception()
  except:
    db["setup"] = True
    state = State()
    server = Server(state)
    state.add_server(server)
    server.set_tilemap(Tilemap())
    server.tilemap.set(Grass(), 0, -1)
    