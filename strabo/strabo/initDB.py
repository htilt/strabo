import sqlite3, os
from contextlib import closing

from strabo import app
# from strabo.database import get_db

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect("test.sqlite3")
  return conn

# This function loads in the proper sql table if it doesn't already exist.
def intiate_db():
  if not os.path.exists("test.sqlite3"):
    with closing(get_db()) as db:
      with app.open_resource('schema.sql', mode='r') as fh:
        db.cursor().executescript(fh.read())
        db.commit()

intiate_db()