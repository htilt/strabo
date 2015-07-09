import sqlite3, os, os.path
from PIL import Image
from contextlib import closing
from flask import Flask, request, render_template, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Set paths, to be called later
DATA_DIRECTORY = app.config['UPLOAD_FOLDER']
NEW_DATA_DIRECTORY = 'static/test_thumbnails/'

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect("bbs.sqlite3")
  return conn

# This function loads in the proper sql table if it doesn't already exist.
def migrate_db():
  with closing(get_db()) as db:
    with app.open_resource('schema.sql', mode='r') as fh:
      db.cursor().executescript(fh.read())
      db.commit()
      '''Do I need to return the connection/cursor the first time the db is connected to?'''
      #return db

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(filename):
  # import desired image from /uploads folder
  img = Image.open(DATA_DIRECTORY + filename)
  # create a thumbnail from desired image
  size = 300, 300
  img.thumbnail(size)
  # save the image under a new filename in thumbnails directory
  imagename = filename.split(".")
  newfilename = imagename[0] + "_thumbnail.jpeg"
  path = NEW_DATA_DIRECTORY
  fullpath = os.path.join(path, newfilename)
  img.save(fullpath)
  # return the filename for the thumbnail
  return newfilename

# Cool thought: with Flask, each view is a function
@app.route("/")
def index():
  # If the 'images' table exists, exit this code block. Otherwise, call migrate_db
  # and import 'images' table.
  if not os.path.exists("bbs.sqlite3"):
  	print ("Migrating the db")
  	return migrate_db()
    #return redirect(url_for('index'))
  else:
    with closing(get_db()) as db:
      # Query db for the 10 rows with the largest id #s (the 10 most recent uploads)
      images = db.execute(
        "SELECT title, img_description, created_at, latitude, longitude, period, interest_point, notes, filename, thumbnail_name FROM images ORDER by id DESC LIMIT 10"
      ).fetchall()
      print(images)
    # Passes values from each image to template as tuple, stored in list-array 'images' 
  return render_template("index.html", images=images)      

@app.route("/post", methods=["POST"])
def post():
  # get input from user according to field. Save those values under similar variable names.
  title = request.form.get('title', None)
  img_description = request.form['img_description']
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  period = request.form['period']
  interest_point = request.form['interest_point']
  notes = request.form['notes']
  file = request.files['file']
  file_name = file.filename
  
  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    # If so, make the filename safe by removing unsupported characters
    filename = secure_filename(file.filename)
    # Move the file form the temporary folder to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Make a thumbnail and store it in the thumbnails directory
    thumbnail_name = make_thumbnail(filename)

  # Create a tuple 'params' containing all of the variables from above. Pass it to the cursor and commit changes.
  with closing(get_db()) as db:
    params = (title, img_description, latitude, longitude, period, interest_point, notes, file_name, thumbnail_name)
    db.cursor().execute("INSERT INTO images(title, img_description, latitude, longitude, period, interest_point, notes, filename, thumbnail_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
    db.commit()

  return redirect(url_for('index'))

if __name__ == "__main__":
  app.debug = True
  app.run()