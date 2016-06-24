### CHANGING THE DATATBASE:

* schema.py
    * If necessary add database column as shown in file.


* run "alembic revision -m revision_name"
* alembic/versions/revision_name.py
    * Edit so that it correctly changes the database to match the new schema
* run "alembic upgrade head"

The database should now run smoothly, assuming the revision file is of the correct format.

Now, to actually adding in is a little trickier.

Updating set_database.py:

* private_helper.py
    * edit the fill_table function
        * input: add an argument of a type that will come from and the html form via flask
        * output: a database row object with all relevant information
* set_database.py
    * add your new feature inputs into the database

In order to edit the admin interface see admin_edit.md
