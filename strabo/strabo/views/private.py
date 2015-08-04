import os
from contextlib import closing

from flask import request, render_template, redirect, url_for
from werkzeug import secure_filename

from strabo import app
from strabo.functions import allowed_file, migrate_db, make_thumbnail, \
get_interest_points, get_events, get_images_flex, get_column_names, search, \
delete, get_all, insert_images, insert_ips, insert_events

# Landing page allows viewer to select amoung tabs to start editing
@app.route("/", methods=["GET"])
def index():
  # If the 'images' table exists, exit this code block. Otherwise, call migrate_db
  # and import 'images' table.
  if not os.path.exists("bbs.sqlite3"):
    migrate_db()
  images = []
  events = []
  interest_points = []
  return render_template("private/base.html")      

###
###
### Views to upload images to db
@app.route("/upload_images/")
def upload_images():
  images = get_images_flex()
  events = get_events()
  interest_points = get_interest_points()
  return render_template("private/upload_images.html", images= images,
    interest_points=interest_points, events=events)

@app.route("/upload_images/post", methods=["POST"])
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

  params = (title, img_description, latitude, longitude, period, 
      interest_point, notes, file_name, thumbnail_name)
  insert_images(params)
  return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/upload_ips/")
def upload_ips():
  interest_points = get_interest_points()
  return render_template("private/upload_ips.html", interest_points=interest_points)

@app.route("/interest_points/post", methods=["POST"])
def interest_points_post():
  name = request.form['name']
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  notes = request.form['notes']
  params = (name, latitude, longitude, notes)
  insert_ips(params)
  return redirect(url_for('index'))

###
###
### Views to add events to the db
@app.route("/upload_events/")
def upload_events():
  events = get_events()
  return render_template("private/upload_events.html", events=events)

@app.route("/events/post", methods=["POST"])
def event_post():
  title = request.form['title']
  event_description = request.form['event_description']
  year = request.form['year']
  notes = request.form['notes']
  params = (title, event_description, year, notes)
  insert_events(params)
  return redirect(url_for('index'))

###
###
### Views to search for and delete images ###
@app.route("/edit_images/")
def edit_images():
  categories = get_column_names('images')
  return render_template("private/edit_images.html", categories=categories)

@app.route("/edit_images/post/", methods=["POST"])
def edit_images_post():
  table_name = 'images'
  column = request.form['categories']
  search_term = request.form['search']
  images = search(table_name, column, search_term)
  categories = get_column_names('images')
  return render_template("private/edit_images.html", images=images, categories=categories)

@app.route("/edit_images/delete/", methods=["POST"])
def edit_images_delete():
  table_name = 'images'
  keys = request.form.getlist('primary_key')
  delete(keys, table_name)
  return redirect(url_for('index'))

###
###
### Views to search for and delete interest points ###
@app.route("/edit_ips/")
def edit_ips():
  categories = get_column_names('interest_points')
  return render_template("private/edit_ips.html", categories=categories)

@app.route("/edit_ips/post/", methods=["POST"])
def edit_ips_post():
  table_name = 'interest_points'
  column = request.form['categories']
  search_term = request.form['search']
  interest_points = search(table_name, column, search_term)
  categories = get_column_names('interest_points')
  return render_template("private/edit_ips.html", interest_points=interest_points, categories=categories)

@app.route("/edit_ips/delete/", methods=["POST"])
def edit_ips_delete():
  table_name = 'interest_points'
  keys = request.form.getlist('primary_key')
  delete(keys, table_name)
  return redirect(url_for('index'))

###
###
### Views to search for and delete events ###
@app.route("/edit_events/")
def edit_events():
  categories = get_column_names('events')
  return render_template("private/edit_events.html", categories=categories)

@app.route("/edit_events/post/", methods=["POST"])
def edit_events_post():
  table_name = 'events'
  column = request.form['categories']
  search_term = request.form['search']
  events = search(table_name, column, search_term)
  categories = get_column_names('events')
  return render_template("private/edit_events.html", events=events, categories=categories)

@app.route("/edit_events/delete/", methods=["POST"])
def edit_events_delete():
  table_name = 'events'
  keys = request.form.getlist('primary_key')
  delete(keys, table_name)
  return redirect(url_for('index'))

