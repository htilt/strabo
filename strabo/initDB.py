from strabo import schema_livy
from strabo import database

# This function loads in the proper sql table if it doesn't already exist.
def intiate_db():
    schema_livy.Base.metadata.create_all(database.engine)

if __name__ == '__main__':
  intiate_db()
# update_tables()
