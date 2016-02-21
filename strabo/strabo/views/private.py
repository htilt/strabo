import os, ast, sys
from contextlib import closing

from flask import request, render_template, redirect, url_for
from werkzeug import secure_filename

from strabo import app
from strabo.database import get_flex, get_column_names, search, \
delete, insert_images, insert_ips, insert_events, get_max_id, edit_image, \
edit_ip, edit_event, get_geojson, insert_text, edit_textselection
from strabo.utils import make_date, DMS_to_Dec, clean_date, prettify_columns, \
get_raw_column, get_fields
from strabo.image_processing import make_thumbnail, allowed_file #, getEXIF
from strabo.geojson import get_coords, get_type, add_name_and_color, \
make_featureCollection
from strabo.filewriting import write_to, rewrite_geojson

# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html", 
    WEBSITE_TITLE=app.config['WEBSITE_TITLE'],
    INDEX_GREETING=app.config['INDEX_GREETING'])      

###
###
### Views to upload images to db
@app.route("/admin/upload_images/")
def upload_images():
  table_name = 'images'
  images = get_flex(table_name, 10)
  events = get_flex('events')
  periods = app.config['PERIODS']
  interest_points = get_flex('interest_points')
  return render_template("private/upload_images.html", images= images,
    interest_points=interest_points, events=events, periods=periods, 
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

# harvest and clean select EXIF data including datetime, lat, long
@app.route("/admin/upload_images/exif/", methods=['POST', 'GET'])
def getEXIF():
  tags = request.form.get('key')
  dicty = ast.literal_eval(tags)
  if 'DateTimeOriginal' in dicty:
    dateTimeOriginal = dicty['DateTimeOriginal']
    # returns a list of split year, month, day
    dateTimeOriginal = clean_date(dateTimeOriginal)
    year = dateTimeOriginal[0]
    month = dateTimeOriginal[1]
    day = dateTimeOriginal[2]
  else: 
    year = None
    month = None
    day = None
  if 'GPSLatitude' in dicty: 
    latitude = dicty['GPSLatitude']
    latitude = DMS_to_Dec(latitude)
  else: latitude = None
  if 'GPSLongitude' in dicty:
    longitude = dicty['GPSLongitude']
    longitude = DMS_to_Dec(longitude)
  else: longitude = None
  return render_template("private/form_images.html", longitude=longitude,
    latitude=latitude, month=month, year=year, day=day)

@app.route("/admin/upload_images/post", methods=["POST"])
def post():
  # get input from user according to field. Save those values under 
  # similar variable names.
  title = request.form.get('title', None)
  img_description = request.form['img_description']
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  period = request.form['period']
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  date_created = make_date(month, day, year)
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''
  file = request.files['file']

  # if administrator does not indicate an interest point or event
  # for the image, fill field with empty string
  if not request.form['interest_point'] == 'Select One':
    interest_point = request.form['interest_point']
  else: interest_point = ''
  if not request.form['event'] == 'Select One':
    event = request.form['event']
  else: event = ''
  if not request.form['period'] == 'Select One':
    period = request.form['period']
  else: period = ''


  # Get primary key for saving filename and thumbnailname
  max_id = get_max_id()
  this_id = max_id + 1

  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    # If so, make the filename safe by removing unsupported characters
    filename = secure_filename(file.filename)
    # prepend unique id to ensure an unique filename
    filename = str(this_id) + '_' + filename
    # Move the file from the temporary folder to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # # Call function to extract EXIF data
    # date_created = getEXIF(app.config['UPLOAD_FOLDER'], filename)
    # Make a thumbnail and store it in the thumbnails directory
    thumbnail_name = make_thumbnail(filename, this_id)

  # insert new db entry
  params = (title, img_description, latitude, longitude, 
    date_created, interest_point, event, period, notes, tags, 
    edited_by, filename, thumbnail_name)
  insert_images(params)
  return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
  interest_points = get_flex('interest_points')
  # get feature types 
  feat_types = app.config["FEATURE_TYPES"]
  return render_template("private/upload_ips.html", 
    interest_points=interest_points, 
    feat_types=feat_types,
    INTPT_FILE=app.config['INTPT_FILE'],
    DRAWMAP_JS=app.config['DRAWMAP_JS'])

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
  # get user input
  name = request.form['name']
  notes = request.form['notes']
  tags = request.form['tags']
  books = request.form['books']
  color = request.form['color']
  # if administrator does not provide feature_type, fill 
  # with empty string
  if not request.form['feature_type'] == 'Select One':
    feature_type = request.form['feature_type']
  else: feature_type = ''
  edited_by = ''
  # if the administrator provides a geojson object, harvest
  # extra data and supply name and color
  if request.form['geojson']:
    geojson_object = request.form['geojson']
    coordinates = str(get_coords(geojson_object))
    geojson_feature_type = str(get_type(geojson_object))
    geojson_object = add_name_and_color(geojson_object, name, color)
  # Otherwise, supply empty string
  else: 
    geojson_object = ''
    coordinates = ''
    geojson_feature_type = ''
    geojson_object = ''

  # insert new db entry
  params = (name, books, coordinates, geojson_object, feature_type, 
    geojson_feature_type, notes, tags, edited_by)
  insert_ips(params)
  # Rewrite geoJSON file according to changes
  rewrite_geojson()
  return redirect(url_for('index'))

###
###
### Views to add events to the db
@app.route("/admin/upload_events/")
def upload_events():
  events = get_flex('events')
  return render_template("private/upload_events.html", events=events)

@app.route("/admin/events/post", methods=["POST"])
def event_post():
  # get user input
  title = request.form['title']
  event_description = request.form['event_description']
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  date_of_event = make_date(month, day, year)

  # insert new db entry
  params = (title, event_description, date_of_event, notes, tags, edited_by)
  insert_events(params)
  return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_text/")
def upload_text():
  text_selections = get_flex('text_selections')
  interest_points = get_flex('interest_points')
  events = get_flex('events')
  return render_template("private/upload_text.html", 
    text_selections=text_selections,
    interest_points=interest_points,
    events=events)

@app.route("/admin/text/post", methods=["POST"])
def text_post():
  # get user input
  name = request.form['name']
  book = request.form['book']
  section = request.form['section']
  pages = request.form['pages']
  passage = request.form['passage']
  interest_point = request.form['interest_point']
  event = request.form['event']
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''
  
  # insert new db entry
  params = (name, book, section, pages, passage, 
    interest_point, event, notes, tags, edited_by)
  insert_text(params)
  return redirect(url_for('index'))

###
###
### Views to search for and delete images ###
@app.route("/admin/delete_images/", methods=["GET"])
def delete_images():
  table_name = 'images'
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  
  # get images from search
  if search_term is None:
    images = get_flex(table_name)
  else:
    images = search(table_name, search_field, search_term)
  return render_template("private/delete_images.html", fields=fields, images=images, 
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/delete_images/delete/", methods=["POST"])
def delete_images_delete():
  table_name = 'images'
  keys = request.form.getlist('primary_key')
  delete(keys, table_name)
  return redirect(url_for('index'))

###
###
### Views to search for and delete interest points ###
@app.route("/admin/delete_ips/", methods=["GET"])
def delete_ips():
  table_name = 'interest_points'
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get interest points from search
  if search_term is None:
    interest_points = get_flex(table_name)
  else:
    interest_points = search(table_name, search_field, search_term)
  return render_template("private/delete_ips.html", fields=fields, 
    interest_points=interest_points)

@app.route("/admin/delete_ips/delete/", methods=["POST"])
def delete_ips_delete():
  # delete selected items from specified table by primary key
  delete(request.form.getlist('primary_key'), 'interest_points')
  # rewrite the file that gets loaded in with geojson objects
  rewrite_geojson()
  return redirect(url_for('index'))

###
###
### Views to search for and delete events ###
@app.route("/admin/delete_events/", methods=["GET"])
def delete_events():
  table_name = 'events'
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get events from search
  if search_term is None:
    events = get_flex(table_name)
  else:
    events = search(table_name, search_field, search_term)
  return render_template("private/delete_events.html", fields=fields, 
    events=events)

@app.route("/admin/delete_events/delete/", methods=["POST"])
def delete_events_delete():
  # delete selected items from specified table by primary key
  delete(request.form.getlist('primary_key'), 'events')
  return redirect(url_for('index'))

###
###
### Views to search for and delete text ###
@app.route("/admin/delete_text/", methods=["GET"])
def delete_text():
  table_name = 'text_selections'
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  # get text selections from search
  if search_term is None:
    text_selections = get_flex(table_name)
  else:
    text_selections = search(table_name, search_field, search_term)
  return render_template("private/delete_text.html", 
    fields=fields, 
    text_selections=text_selections)

@app.route("/admin/delete_text/delete/", methods=["POST"])
def delete_text_delete():
  # delete selected items from specified table by primary key
  delete(request.form.getlist('primary_key'), 'text_selections')
  return redirect(url_for('index'))

###
###
### Views to search for and edit images ###
@app.route("/admin/edit_images/", methods=["GET"])
def edit_images():
  table_name = 'images'
  
  # if administrator clicks edit button on an image
  # return editing form with prior values
  if request.args.get('edit-btn'):
    image = search(table_name, 'id', request.args.get('edit-btn'))
    date_created = image[0]['date_created']
    date_created = clean_date(date_created)
    year = date_created[0]
    month = date_created[1]
    day = date_created[2]
    events = get_flex('events')
    interest_points = get_flex('interest_points')

    # get periods
    periods = app.config['PERIODS']

    return render_template("private/complete_form_images.html", image=image,
      events=events, interest_points=interest_points, year=year, month=month, 
      day=day, periods=periods, 
      UPLOAD_FOLDER_RELPATH=app.config['UPLOAD_FOLDER_RELPATH'])

  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  

  # get images from search
  if search_term is None:
    images = get_flex(table_name)
  else:
    images = search(table_name, search_field, search_term)
  return render_template("private/edit_images.html", 
    fields=fields, images=images, 
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/edit_images/edit/", methods=["POST"])
def edit_images_edit():
  # get new input from user to substitute for old content
  title = request.form.get('title', None)
  img_description = request.form['img_description']
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  period = request.form['period']
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  date_created = make_date(month, day, year)
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''

  # if administrator does not indicate an interest point or event
  # for the image, fill field with empty string
  if not request.form['interest_point'] == 'Select One':
    interest_point = request.form['interest_point']
  else: interest_point = ''
  if not request.form['event'] == 'Select One':
    event = request.form['event']
  else: event = ''
  if not request.form['period'] == 'Select One':
    period = request.form['period']
  else: period = ''

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  image = search('images', 'id', key)
  created_at = image[0]['created_at']
  thumbnail_name = image[0]['thumbnail_name']
  filename = image[0]['filename']  

  # edit db entry
  params = (key, created_at, title, img_description, latitude, longitude, 
    date_created, interest_point, event, period, notes, tags, edited_by, 
    filename, thumbnail_name)
  edit_image(params)
  return redirect(url_for('index'))

###
###
### Views to search for and edit interest points ###
@app.route("/admin/edit_ips/", methods=["GET"])
def edit_ips():
  table_name = 'interest_points'
  
  feat_types = app.config['FEATURE_TYPES']
  # if administrator clicks edit button on an interest point
  if request.args.get('edit-btn'):
    interest_point = search(table_name, 'id', request.args.get('edit-btn'))
    return render_template("private/form_ips.html", feat_types=feat_types,
      interest_point=interest_point)

  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  
  # get interest points from search
  if search_term is None:
    interest_points = get_flex(table_name)
  else:
    interest_points = search(table_name, search_field, search_term)

  return render_template("private/edit_ips.html", fields=fields, 
    interest_points=interest_points)

@app.route("/admin/edit_ips/edit/", methods=["POST"])
def edit_ips_edit():
  # get new input from user to substitute for old content
  name = request.form['name']
  books = request.form['books']
  notes = request.form['notes']
  tags = request.form['tags']
  feature_type = request.form['feature_type']
  coordinates = request.form['coordinates']
  geojson_object = request.form['geojson_object']
  edited_by = ''

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  ip = search('interest_points', 'id', key)
  created_at = ip[0]['created_at']
  geojson_feature_type = ip[0]['geojson_feature_type']

  # edit db entry
  params = (key, created_at, name, books, coordinates, 
    geojson_object, feature_type, geojson_feature_type, 
    notes, tags, edited_by)
  edit_ip(params)
  # rewrite geojson file
  rewrite_geojson()
  return redirect(url_for('index'))

###
###
### Views to search for and edit events ###
@app.route("/admin/edit_events/", methods=["GET"])
def edit_events():
  table_name = 'events'

  # if administrator clicks edit button on an event
  if request.args.get('edit-btn'):
    event = search(table_name, 'id', request.args.get('edit-btn'))
    date_of_event = event[0]['date_of_event']
    date_of_event = clean_date(date_of_event)
    year = date_of_event[0]
    month = date_of_event[1]
    day = date_of_event[2]
    return render_template("private/form_events.html", 
      event=event, year=year, month=month, day=day)
  
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  
  # get events from search
  if search_term is None:
    events = get_flex(table_name)
  else:
    events = search(table_name, search_field, search_term)
  
  return render_template("private/edit_events.html", fields=fields, 
    events=events)

@app.route("/admin/edit_events/edit/", methods=["POST"])
def edit_events_edit():
  # get new input from user to substitute for old content
  title = request.form['title']
  event_description = request.form['event_description']
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  date_of_event = make_date(month, day, year)

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  event = search('events', 'id', key)
  created_at = event[0]['created_at']
  
  # edit db entry
  params = (key, created_at, title, event_description, date_of_event, notes, 
    tags, edited_by)
  edit_event(params)
  return redirect(url_for('index'))

###
###
### Views to search for and edit text selections ###
@app.route("/admin/edit_text/", methods=["GET"])
def edit_text():
  table_name = 'text_selections'
  events = get_flex('events')
  interest_points = get_flex('interest_points')

  # if administrator clicks edit button on a text selection
  if request.args.get('edit-btn'):
    text_selection = search(table_name, 'id', request.args.get('edit-btn'))
    return render_template("private/form_text.html", events=events,
      interest_points=interest_points, text_selection=text_selection)

  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)
  
  # get text selections from search
  if search_term is None:
    text_selections = get_flex(table_name)
  else:
    text_selections = search(table_name, search_field, search_term)
  
  return render_template("private/edit_text.html", 
    fields=fields, 
    text_selections=text_selections)

@app.route("/admin/edit_text/edit/", methods=["POST"])
def edit_text_edit():
  # get new input from user to substitute for old content
  name = request.form['name']
  book = request.form['book']
  section = request.form['section']
  pages = request.form['pages']
  passage = request.form['passage']
  interest_point = request.form['interest_point']
  event = request.form['event']
  notes = request.form['notes']
  tags = request.form['tags']
  edited_by = ''

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  text_selection = search('text_selections', 'id', key)
  created_at = text_selection[0]['created_at']

  # edit db entry
  params = (key, created_at, name, book, section, pages, passage,
    interest_point, event, notes, tags, edited_by)
  edit_textselection(params)
  return redirect(url_for('index'))

