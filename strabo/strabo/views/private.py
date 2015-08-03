import os
from contextlib import closing

from flask import request, render_template, redirect, url_for
from werkzeug import secure_filename

from strabo import app
from strabo.functions import allowed_file, get_db, migrate_db, make_thumbnail, get_interest_points, get_events, get_images_flex, get_column_names, search_images, delete

# Cool thought: with Flask, each view is a function
@app.route("/", methods=["GET", "POST"])
def index():
  # If the 'images' table exists, exit this code block. Otherwise, call migrate_db
  # and import 'images' table.
  if not os.path.exists("bbs.sqlite3"):
    migrate_db()
  images = []
  events = []
  interest_points = []
  return render_template("private/base.html")      

@app.route("/upload_images/")
def upload_images():
  images = get_images_flex()
  events = get_events()
  interest_points = get_interest_points()
  return render_template("private/upload_images.html", images= images, interest_points=interest_points, event=events)

@app.route("/upload_ips/")
def upload_ips():
  interest_points = get_interest_points()
  return render_template("private/upload_ips.html", interest_points=interest_points)

@app.route("/upload_events/")
def upload_events():
  events = get_events()
  return render_template("private/upload_events.html", events=events)

@app.route("/edit_images/")
def edit_images():
  categories = get_column_names('images')
  return render_template("private/edit_images.html", categories=categories)

@app.route("/edit_ips/")
def edit_ips():
  return render_template("private/edit_ips.html")

@app.route("/edit_events/")
def edit_events(): 
  return render_template("private/edit_events.html")

@app.route("/image/post", methods=["POST"])
def post():
  # get input from user according to field. Save those values under similar variable names.
  title = request.form.get('title', None)
  img_description = request.form['img_description']
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  period = request.form['period']
  notes = request.form['notes']
  file = request.files['file']
  file_name = file.filename
  if not request.form['interest_point'] == 'Select One':
    interest_point = request.form['interest_point']
  else: interest_point = ''

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

@app.route("/edit_images/post/", methods=["POST"])
def edit_images_post():
  column = request.form['categories']
  search_term = request.form['search']
  images = search_images(column,search_term)
  categories = get_column_names('images')
  return render_template("private/edit_images.html", images=images, categories=categories)

@app.route("/edit_images/delete/", methods=["POST"])
def edit_images_delete():
  # Account for null value possibility
  keys = request.form.getlist('primary_key')
  print (keys)
  delete(keys)
  return redirect(url_for('index'))















# @app.route("/events/post", methods=["POST"])
# def event_post():
#   title = request.form['title']
#   event_description = request.form['event_description']
#   year = request.form['year']
#   notes = request.form['notes']

#   with closing(get_db()) as db:
#     params = (title, event_description, year, notes)
#     db.cursor().execute("INSERT INTO events(title, event_description, year, notes) VALUES(?, ?, ?, ?)", params)
#     db.commit()

#   return redirect(url_for('index'))

# @app.route("/interest_points/post", methods=["POST"])
# def interest_points_post():
#   name = request.form['name']
#   latitude = request.form['latitude']
#   longitude = request.form['longitude']
#   notes = request.form['notes']

#   with closing(get_db()) as db:
#     params = (name, latitude, longitude, notes)
#     db.cursor().execute("INSERT INTO interest_points(name, latitude, longitude, notes) VALUES(?, ?, ?, ?)", params)
#     db.commit()

#   return redirect(url_for('index'))
