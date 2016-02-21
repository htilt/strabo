import sqlite3, os
from contextlib import closing

# This function starts a new connection to a database.
def conn_db():
  conn = sqlite3.connect('livy.sqlite3')
  return conn

# This function loads in the proper sql table if it doesn't already exist.
def intiate_db():
  if not os.path.exists('livy.sqlite3'):
    with closing(conn_db()) as db:
      with open("strabo/schema-livy.sql", mode='r') as fh:
        db.cursor().executescript(fh.read())
        db.commit()

# This function could be used to update tables if sqlite schema were
# to be altered
def update_tables():
  with closing(conn_db()) as db:
      with open("strabo/schema-livy.sql", mode='r') as fh:
        db.cursor().executescript(fh.read())
        db.commit()

if __name__ == '__main__':
  intiate_db()
# update_tables()