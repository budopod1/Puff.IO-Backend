from database import db
from state import State
from server import Server
from tiles import Tilemap, Grass

# db()["setup"] = False


def load_state():
  global main_server
  try:
    if not db()["setup"]:
      raise Exception()
  except:
    db()["saves"] = []
    state = State()
    main_server = setup_server(state)
    state.add_server(main_server)
    save_state(state)
    db()["setup"] = True
  loaded = State.load(db()["saves"][::-1][0])
  return loaded


def save_state(state):
  db()["saves"].append(state.save())


def setup_server(state):
  server = Server(state)
  server.set_tilemap(Tilemap())
  server.tilemap.set(Grass(), 0, -1)
  return server
    