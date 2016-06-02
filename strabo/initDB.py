from strabo import db
from strabo import schema

if __name__ == '__main__':
    # This function loads in the proper sql table
    db.create_all()
    db.session.commit()
# update_tables()
