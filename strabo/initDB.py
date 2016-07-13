from strabo import schema
from strabo import config_canyon
from strabo import database

from strabo import db

if __name__ == '__main__':
    config_canyon.config_app(app)
    # This function loads in the proper sql
    schema.Base.metadata.create_all(db.engine)
    db.session.commit()
