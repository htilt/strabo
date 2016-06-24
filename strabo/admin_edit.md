### ADDING FEATURES TO ADMIN INTERFACE:

Add feature to database as explained in db_edit.py

* private.py
    * Change upload_table function to have default value in argument list
    * Change show_table_upload_form to get additional information needed for feature and pass it to render_template
    * Change upload_images.html so that it displays a input form so that you can edit the feature and also give it a default value that comes from the database row so that editing will work.
    * Add feature to edit_table.html so that one can see the value there.
    * Change table_post so that it adds in html form value into private_helper's fill_table function.
