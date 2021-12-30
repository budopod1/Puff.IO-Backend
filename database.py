import json
from replit import db as _db
from time import sleep
from threading import Thread
import requests

_database = {}
upload_continuously_thread = None
_shutdown = False


def database_shutdown():
  global _shutdown
  _shutdown = True


def db():
  return _database


def upload_database():
  try:
    _db["database"] = json.dumps(_database)
  except requests.HTTPError:
    upload_database()


def _download_database():
  try:
    return json.loads(_db["database"])
  except KeyError:
    return {}


def download_database():
  global _database
  _database = _download_database()


def upload_continuously():
  global upload_continuously_thread
  def _upload_continuously():
    while True:
      if _shutdown:
        return
      upload_database()
      sleep(5)
  upload_continuously_thread = Thread(target=_upload_continuously)
  upload_continuously_thread.start()


def reset_database():
  answer = input("WARNING: Are you sure you want to wipe the entire database (y/n) ")
  if answer.lower() == "y":
    for key in _db.keys():
      del _db[key]


reset_database()
