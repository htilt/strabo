This is the README for `strabo`, a database-backed website for
making an interactive map incorporating text and images. 

Last Updated: June 26, 2016

#

Overview
========
`strabo` is a tool designed to offer an administrator an easy method 
for displaying three kinds of information on a website: interest points, images, and textual selections, and for visually relating these pieces of information. 

An administrator can locate interest points on an interactive map and associate textual descriptions and multiple images with each point. 
Once information has been uploaded to the database, it will
be available on a public end of the site. This public end
includes an interactive map that displays interest point markers that, upon being clicked, open a popup with descriptive text and associated photos corresponding to the point of interest. 

See the *Reed Canyon Map* for an example of a website developed using `strabo`.

#

Contents
========
The root directory `strabo` includes subdirectories corresponding to
* `alembic`, a Python data migration tool 
* `docs`, the collection of Sphinx- and JSDoc-generated documentation for the project, including a link to outputted HTML pages
* `test`, a repository of tests using PyTest, Mocha, and Chai

#

Website Set-Up
==============

To run app.py:

1. Make sure that you've installed the progams and modules in 
`requirements.txt`.

2. Make a new directory called 'uploads' within the 'static' 
directory in order to store images uploaded through the 
browser interaction. You should also make a new directory 
'test_thumbnails' within the 'static' directory in order to 
hold the thumbnails generated through browser interaction.

***As the tool is currently designed, images are not stored in 
the SQL database, but rather in a separate folder on the server. 
Image filenames are stored in the database, along with their 
associated metadata.***

3. Edit config.py with your website's specifications.

4. Run initDB.py

5. Run runserver.py

#

_The data migration tool (Alembic) and documentation generating engines (Sphinx and JSDoc) must be installed and configured separately. See their websites for instructions on how to do so._

#

License
=======
Property of Reed College, 2016.
