from strabo import schema
from strabo import database

from strabo import db

if __name__ == '__main__':
    # This function loads in the proper sql
    schema.Base.metadata.create_all(db.engine)
    db.session.commit()
