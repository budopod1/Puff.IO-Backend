from datetime import datetime
import sys
import traceback
from threading import Thread
from time import sleep
from database import db

queue = []
queue_thread = None
_shutdown = False
is_db_setup = False


def log_shutdown():
  global _shutdown
  _shutdown = True


def setup_db():
  global is_db_setup, queue_thread
  try:
    if not db()["setup_log"]:
      raise Exception()
  except:
    db()["setup_log"] = True
    db()["log"] = ""
  queue_thread = Thread(target=write_db)
  queue_thread.start()
  is_db_setup = True


def log(websocket, *messages, is_error=False):
  now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  message = " ".join(messages)
  try:
    address = websocket.remote_address[0]
  except OSError:
    address = "Closed Socket"
  except AttributeError:
    address = "Not in Socket"

  output = message if is_error else f"{address} - [{now}] {message}"
  if is_error:
    print(output, file=sys.stderr)
    log_to_file(output[:-1])
  else:
    log_to_file(output)
    print(output)


def log_to_file(text):
  if not is_db_setup:
    setup_db()
  queue.append(text)


def write_db():
  global queue
  while True:
    if _shutdown:
      break
    try:
      sleep(10)
      if queue:
        db()["log"] += queue.pop() + "\n"
    except IndexError:
      log(None, "Pop from empty list?", is_error=True)


def read_from_file():
  return db()["log"]


def error():
  log(None, traceback.format_exc(), is_error=True)
