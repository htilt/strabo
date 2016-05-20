import os, ast, sys
from contextlib import closing
from strabo import utils

from flask import request, render_template, redirect, url_for
from werkzeug import secure_filename

from strabo import app
from strabo import database
from strabo import schema_livy
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
  itable = schema_livy.Images
  images = database.get_flex(itable, 10)
  events = database.get_flex(itable,'events')
  periods = app.config['PERIODS']
  interest_points = database.get_flex(itable,'interest_points')
  return render_template("private/upload_images.html", images= images,
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
  params = dict()
  params["title"] = request.form.get('title', None)
  params["img_description"] = request.form['img_description']
  params["latitude"] = request.form['latitude']
  params["longitude"] = request.form['longitude']
  params["period"] = request.form['period']
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  params["date_created"] = make_date(month, day, year)
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''
  file = request.files['file']

  # if administrator does not indicate an interest point or event
  # for the image, fill field with empty string
  params["interest_point"] = utils.clear_sel(request.form['interest_point'])
  params["event"] = utils.clear_sel(request.form['event'])
  params["period"] = utils.clear_sel(request.form['period'])

  # Get primary key for saving filename and thumbnailname
  max_id = database.get_max_id()
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
    params["thumbnail_name"] = make_thumbnail(filename, this_id)
    params["filename"] = filename
  else:
      #todo: put this error in the frontend instead of here
      raise RuntimeError("file extension not allowed")

  # insert new db entry
  database.add_to_table(schema_livy.Images,params)
  return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
  interest_points = database.get_flex(schema_livy.InterestPoints)
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
  params = dict()
  params["name"] = request.form['name']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["books"] = request.form['books']
  params["color"] = request.form['color']
  # if administrator does not provide feature_type, fill
  # with empty string
  params["feature_type"] = utils.clear_sel(request.form['feature_type'])
  params["edited_by"] = ''
  # if the administrator provides a geojson object, harvest
  # extra data and supply name and color
  is_gg = bool(request.form['geojson'])
  params["geojson_object"] = request.form['geojson'] if is_gg else ''
  params["coordinates"] = str(get_coords(geojson_object))  if is_gg else ''
  params["geojson_feature_type"] = str(get_type(geojson_object)) if is_gg else ''
  params["geojson_object"] = add_name_and_color(geojson_object, name, color) if is_gg else ''

  # insert new db entry
  database.add_to_table(schema_livy.InterestPoints, params)
  # Rewrite geoJSON file according to changes
  rewrite_geojson()
  return redirect(url_for('index'))

###
###
### Views to add events to the db
@app.route("/admin/upload_events/")
def upload_events():
  events = database.get_flex(schema_livy.Events)
  return render_template("private/upload_events.html", events=events)

@app.route("/admin/events/post", methods=["POST"])
def event_post():
  # get user input
  params["title"] = request.form['title']
  params["event_description"] = request.form['event_description']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  params["date_of_event"] = make_date(month, day, year)

  # insert new db entry
  database.add_to_table(schema_livy.Events,params)
  return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_text/")
def upload_text():
  text_selections = database.get_flex(schema_livy.TextSelections)
  interest_points = database.get_flex(schema_livy.InterestPoints)
  events = database.get_flex(schema_livy.Events)
  return render_template("private/upload_text.html",
    text_selections=text_selections,
    interest_points=interest_points,
    events=events)

@app.route("/admin/text/post", methods=["POST"])
def text_post():
  # get user input
  params = dict()
  params["name"] = request.form['name']
  params["book"] = request.form['book']
  params["section"] = request.form['section']
  params["pages"] = request.form['pages']
  params["passage"] = request.form['passage']
  params["interest_point"] = request.form['interest_point']
  params["event"] = request.form['event']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''

  # insert new db entry
  database.add_to_table(schema_livy.TextSelections,params)

  return redirect(url_for('index'))

###
###
### Views to search for and delete images ###
@app.route("/admin/delete_images/", methods=["GET"])
def delete_images():
  # get search fields
  fields = get_fields(schema_livy.Images)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get images from search
  if search_term is None:
    images = database.get_flex(schema_livy.Images)
  else:
    images = database.search(schema_livy.Images, search_field, search_term)
  return render_template("private/delete_images.html", fields=fields, images=images,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/delete_images/delete/", methods=["POST"])
def delete_images_delete():
  keys = request.form.getlist('primary_key')
  delete(keys, schema_livy.Images)
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
    interest_points = database.get_flex(schema_livy.InterestPoints)
  else:
    interest_points = database.search(schema_livy.InterestPoints, search_field, search_term)
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
  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get events from search
  if search_term is None:
    events = database.get_flex(schema_livy.Events)
  else:
    events = database.search(schema_livy.Events, search_field, search_term)
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
    text_selections = database.get_flex(schema_livy.TextSelections)
  else:
    text_selections = database.search(schema_livy.TextSelections, search_field, search_term)
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
    image = database.search(schema_livy.Images, 'id', request.args.get('edit-btn'))
    date_created = image[0]['date_created']
    date_created = clean_date(date_created)
    year = date_created[0]
    month = date_created[1]
    day = date_created[2]
    events = database.get_flex(schema_livy.Events)
    interest_points = database.get_flex(schema_livy.InterestPoints)

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
    images = database.get_flex(schema_livy.Images)
  else:
    images = database.search(schema_livy.Images, search_field, search_term)
  return render_template("private/edit_images.html",
    fields=fields, images=images,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/edit_images/edit/", methods=["POST"])
def edit_images_edit():
  # get new input from user to substitute for old content
  params = dict()
  params["title"] = request.form.get('title', None)
  params["img_description"] = request.form['img_description']
  params["latitude"] = request.form['latitude']
  params["longitude"] = request.form['longitude']
  params["period"] = request.form['period']
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  params["date_created"] = make_date(month, day, year)
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''

  # if administrator does not indicate an interest point or event
  # for the image, fill field with empty string
  params["interest_point"] = utils.clear_sel(request.form['interest_point'])
  params["event"] = utils.clear_sel(request.form['event'])
  params["period"] = utils.clear_sel(request.form['period'])

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  image = database.search('images', 'id', key)
  params["created_at"] = image[0]['created_at']
  params["thumbnail_name"] = image[0]['thumbnail_name']
  params["filename"] = image[0]['filename']

  # edit db entry
  database.edit_table_key(schema_livy.Images,key,params)
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
    interest_point = database.search(schema_livy.InterestPoints, 'id', request.args.get('edit-btn'))
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
    interest_points = database.get_flex(schema_livy.InterestPoints)
  else:
    interest_points = database.search(schema_livy.InterestPoints, search_field, search_term)

  return render_template("private/edit_ips.html", fields=fields,
    interest_points=interest_points)

@app.route("/admin/edit_ips/edit/", methods=["POST"])
def edit_ips_edit():
  params = dict()
  # get new input from user to substitute for old content
  params["name"] = request.form['name']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["books"] = request.form['books']
  params["feature_type"] = request.form['feature_type']
  params["coordinates"] = request.form['coordinates']
  params["geojson_object"] = request.form['geojson_object']
  params["edited_by"] = ''

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  ip = database.search('interest_points', 'id', key)
  params["created_at"] = ip[0]['created_at']
  params["geojson_feature_type"] = ip[0]['geojson_feature_type']

  # edit db entry
  database.edit_table_key(schema_livy.InterestPoints,key,params)
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
    event = database.search(schema_livy.Events, 'id', request.args.get('edit-btn'))
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
    events = database.get_flex(schema_livy.Events)
  else:
    events = database.search(schema_livy.Events, search_field, search_term)

  return render_template("private/edit_events.html", fields=fields,
    events=events)

@app.route("/admin/edit_events/edit/", methods=["POST"])
def edit_events_edit():
  # get new input from user to substitute for old content
  params["title"] = request.form['title']
  params["event_description"] = request.form['event_description']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  params["date_of_event"] = make_date(month, day, year)

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  event = database.search('events', 'id', key)
  params["created_at"] = event[0]['created_at']

  # edit db entry
  database.edit_table_key(schema_livy.Events,key,params)
  edit_event(key,params)
  return redirect(url_for('index'))

###
###
### Views to search for and edit text selections ###
@app.route("/admin/edit_text/", methods=["GET"])
def edit_text():
  table_name = 'text_selections'
  events = database.get_flex(schema_livy.Events)
  interest_points = database.get_flex(schema_livy.InterestPoints)

  # if administrator clicks edit button on a text selection
  if request.args.get('edit-btn'):
    text_selection = database.search(schema_livy.TextSelections, 'id', request.args.get('edit-btn'))
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
    text_selections = database.get_flex(schema_livy.TextSelections)
  else:
    text_selections = database.search(schema_livy.TextSelections, search_field, search_term)

  return render_template("private/edit_text.html",
    fields=fields,
    text_selections=text_selections)

@app.route("/admin/edit_text/edit/", methods=["POST"])
def edit_text_edit():
  # get new input from user to substitute for old content
  params = dict()
  params["name"] = request.form['name']
  params["book"] = request.form['book']
  params["section"] = request.form['section']
  params["pages"] = request.form['pages']
  params["passage"] = request.form['passage']
  params["interest_point"] = request.form['interest_point']
  params["event"] = request.form['event']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''

  # retrieve pieces of info for image that should not be edited
  key = request.form['edit-btn']
  params["text_selection"] = database.search('text_selections', 'id', key)
  params["created_at"] = text_selection[0]['created_at']

  # edit db entry
  database.edit_table_key(schema_livy.TextSelections,key,params)

  return redirect(url_for('index'))
