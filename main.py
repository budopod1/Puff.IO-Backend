import asyncio
import websockets
import websockets.exceptions
import json
from time import perf_counter, sleep
from random import random
from threading import Thread

import log
from user import User
from tiles import Tilemap, Grass
from entities import Player


class State:
  def __init__(self):
    # Manage the global state off the whole MMO
    self.time_delta = 0
    self.last_tick = 0
    self.users = {}
  
  def tick(self):
    self.time_delta = perf_counter() - self.last_tick
    self.last_tick = perf_counter()


class Server:
  def __init__(self, state):
    # Manage a single server
    self.state = state
    self.tilemap = None
    self.background = "black"
    self.images = []
    self.entities = []
  
  def set_tilemap(self, tilemap):
    self.tilemap = tilemap
  
  def tick(self):
    self.images = []
    self.background = "black"

  def render(self):
    return {"background": self.background, "images": self.images}


state = State()
server = Server(state)
done_server = {}
server.set_tilemap(Tilemap(server))
server.tilemap.set(Grass(), 0, -1)


def ticker():
  global done_server
  try:
    log.log(None, "Game starting...")
    while True:
      state.tick()
      server.tick()
      server.tilemap.render()
      server.background = "#16f4f7"
      usernames = []

      for entity in server.entities:
        if isinstance(entity, Player):
          usernames.append(entity.username)
        entity.frame()
        if entity.active:
          server.images.append(entity.render())

      for username in state.users.keys():
        if username not in usernames:
          server.entities.append(Player(server, 0, 2, state.users[username]))

      for user in state.users.values():
        user.frame()

      done_server = server.render()
      sleep(0.0001)
  except:
    log.error()


async def main(websocket, path):
  try:
    log.log(websocket, "New connection")

    # Store the last password entered
    last_password = ""
    last_username = ""

    success = False
    data = json.loads(await websocket.recv())
    message = "unkown error!"
    # Make sure all necessary data is sent
    if set(data.keys()) != {"username", "password", "connnectType"}:
      log.log(websocket, f"Message corrupt: '{data}'")
      await websocket.send(json.dumps({"type": "error", "data": "Message corrupt"}))
      await websocket.close()
      return
    
    # Pervent hashing timing attacks
    await asyncio.sleep(random())
    
    # Do signin/signup
    username = data["username"]
    password = data["password"]
    if data["connnectType"] == "signin":
      if username in state.users.keys():
        user = state.users[username]
        if user.check(password.encode('utf8')):
          last_username = username
          last_password = password
          log.log(websocket, "Signin successful into account:", username)
          success = True
        else:
          message = "Password is incorrect"
      else:
        message = "Username is not valid"
    elif data["connnectType"] == "signup":
      if username not in state.users.keys():
        if 2 <= len(username) <= 20:
          if 8 <= len(password):
            if username == "LOG":
              log.log(websocket, "WARNING: Signup to account LOG!")
            user = User(username, password.encode('utf8'))
            user.change_server(server)
            state.users[username] = user
            last_username = username
            last_password = password
            log.log(websocket, "Signup successful into account:", username)
            success = True
          else:
            message = "Password must be >8 and <100 charechters"
        else:
          message = "Username must be >3 and <20 charechters"
      else:
        message = "User already exists"
    else:
      message = "Corrupt signin/signup attempt"
    if not success:
      # Return error message
      log.log(websocket, f"Signin/Signup incorrect into account: '{username}'")
      await websocket.send(json.dumps({"type": "error", "data": message}))
      await websocket.close()
      return

    # Do log mode
    if username == "LOG":
      log.log(websocket, "Read from log")
      await websocket.send(json.dumps({"type": "error", "data": log.read_from_file()}))
      await websocket.close()
      return

    # Main server websocket loop
    while True:
      data = json.loads(await websocket.recv())
      if set(data.keys()) != {"username", "password", "keys_down", "just_down"}:
        log.log(websocket, f"Message corrupt: '{data}'")
        await websocket.send(json.dumps({"type": "error", "data": "Message corrupt"}))
        await websocket.close()
        return
      
      success = False
      message = "unkown error!"
      if data["username"] == last_username:
        user = state.users[data["username"]]
        if last_password == data["password"]:
          user.update(data)
          success = True
        else:
          message = "Message corrupt"
      else:
        message = "Message corrupt"
      if not success:
        log.log(websocket, "Message corrupt with username:", data["username"])
        await websocket.send(json.dumps({"type": "error", "data": message}))
        await websocket.close()
        return
      
      await websocket.send(json.dumps({"type": "frame", "data": done_server, "camera": state.users[data["username"]].camera.render()}))
  except (websockets.exceptions.ConnectionClosedOK, OSError, websockets.exceptions.ConnectionClosedError):
    log.log(websocket, "Going away:", data["username"])
  except:
    log.error()


def start():
  log.log(None, "Server starting...")
  start_server = websockets.serve(main, '0.0.0.0', 5678)
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
  ticker_thread = Thread(target=ticker)
  ticker_thread.start()
  start()
