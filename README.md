
This is the README for *Strabo*, a database-backed website for
making an interactive map incorporating text and images. 

Last Updated: August 1, 2016

#

Overview
--------
Strabo is a tool designed to offer an administrator an easy method 
for displaying three kinds of information on a website - points of interest, images, and texts - and for visually relating these pieces of information. 

An administrator can locate points of interest on an interactive map and associate textual descriptions and images with each point. 
Once information has been uploaded to the database, it will
be available on a public end of the site. This public end
includes an interactive map that displays interest point markers that, upon being clicked, open a popup with descriptive text and  photos corresponding to the point of interest. 

See the **Reed Canyon Map** for an example of a website developed using Strabo.

#

Strabo Contents
---------------
The root directory **strabo** includes subdirectories corresponding to

- ``alembic``, a Python data migration tool 

- ``docs``, the collection of Sphinx-generated documentation for the project, which can be found at [Read the Docs](http://strabo.readthedocs.io/en/latest/)

- ``strabo``, the directory of HTML, CSS, Python, and Javascript that set up the website

- ``test``, a repository of tests using PyTest, Mocha, and Chai

#

Website Set-Up
--------------

1. Make sure that you've installed the programs and modules in ``requirements.txt``.

2. Make a new directory called 'uploads' within the 'static' directory in order to store images uploaded through the browser interaction. You should also make a new directory 'test_thumbnails' within the 'static' directory in order to hold the thumbnails generated through browser interaction.

***As the tool is currently designed, images are not stored in 
the SQL database, but rather in a separate folder on the server. 
Image filenames are stored in the database, along with their 
associated metadata.***

3. Edit ``config.py`` with your website's specifications.

4. Run ``initDB.py``

5. Run ``runserver.py``



*The data migration tool (Alembic) and documentation generating engine (Sphinx) must be installed and configured separately. See their websites for instructions on how to do so.*

#

License
-------
Property of Reed College, 2016.
