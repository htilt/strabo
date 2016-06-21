from strabo import db
from strabo import schema

if __name__ == '__main__':
    # This function loads in the proper sql
    schema.Base.metadata.create_all(db.engine)
    db.session.commit()
# update_tables()
