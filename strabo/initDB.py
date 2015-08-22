import sqlite3, os
from contextlib import closing

# This function starts a new connection to a database.
def conn_db():
  conn = sqlite3.connect('bbs.sqlite3')
  return conn

# This function loads in the proper sql table if it doesn't already exist.
def intiate_db():
  if not os.path.exists('bbs.sqlite3'):
    with closing(conn_db()) as db:
      with open("strabo/schema.sql", mode='r') as fh:
        db.cursor().executescript(fh.read())
        db.commit()

intiate_db()