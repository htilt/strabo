This is the readme for the Canyon Uploader tool.
Last Updated: July 9, 2015

To run app.py, make sure that you've installed the 
progams and modules in requirements.txt.

Additionally, you should make a new directory
called 'uploads' within the primary directory in 
order to store images uploaded through the browser
interaction. You should additionally make a new
directory 'test_thumnails' within the 'static' 
directory in order to hold the thumbnails generated 
through browser interaction.

This tool is designed to offer a user a method 
for uploading images to a database. The browser
should display the most recent 10 images that the 
user has uploader along with their associated metadata.

As the tool is currently designed, images are not
stored in the SQL database, but rather in a separate 
folder on the server. Image filenames are stored in the 
database, along with their associated metadata.

