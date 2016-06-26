This is the readme for strabo, a database-backed website for
making an interactive map incorporating text and images. 

Last Updated: January 8, 2016

#
#
#
#
Website Features

This tool is designed to offer an administrator an easy method 
for uploading four kinds of information to a database: images, 
events, interest points, and textual selections, and for relating
these pieces of information. Events and interest points, once
uploaded, will populate the dropdown seletion for images so that
an administrator can associate images with an event and/or 
interest point. These images will then be displayed when a user
clicks on an interest point in the map. ***Currently the timeline is
disabled, although future releases will (hopefully) make it such 
that images associated with events will also be displayed in the 
timeline.*** Below the upload interface a table will display the 
most recent 10 images, interest points, events, or textual selections
that the administrator has uploader along with their associated 
metadata.

Once information has been uploaded to the database, it will
be available on a public end of the site. This public end
includes an interactive map, image gallery, and timeline 
(currently disabled). As of the January 2016 update, the map
only displays six images at a time. To view additional images, the 
user is redirected to the image gallery with the apporpriate search
query.

#
#
#
#
Website Set-Up

To run app.py:

1. Make sure that you've installed the progams and modules in 
requirements.txt.

2. Make a new directory called 'uploads' within the 'static' 
directory in order to store images uploaded through the 
browser interaction. You should also make a new directory 
'test_thumnails' within the 'static' directory in order to 
hold the thumbnails generated through browser interaction.

***As the tool is currently designed, images are not stored in 
the SQL database, but rather in a separate folder on the server. 
Image filenames are stored in the database, along with their 
associated metadata.***

3. Edit config.py with your website's specifications.

4. Run initDB.py

5. Run runserver.py
