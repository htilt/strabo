## Database file structure

 * schema.py
    * Defines the database structure with sqlalchemy's model class
        * Takes the place of sql's CREATE TABLE statement
        * Defines relationships between tables
    * Deals with database metadata
        * Where you store list of tables
        * Stores relationships between tables and columns
 * initDB.py
    * Creates the database tables as defined in schema.py *if they do not already exist*
 * database.py
    * Helper file so that other files do not have to know the internals of sqlachemy
 * private_helper.py and public_helper.py
    * Acts as a bridge between html forms as displayed in the admin interface and the database/outgoing flask forms
        * Inputs should be flask form items
        * Outputs should be useable by flask or the database
        * Side affects should probably be somewhere else
