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
from strabo.geojson_wrapper import get_coords, get_type, add_name_and_color, get_all_feature_collections

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
  images = database.get_rows(schema_livy.Images, 10)
  events = database.get_all_rows(schema_livy.Events)
  periods = app.config['PERIODS']
  interest_points = database.get_all_rows(schema_livy.InterestPoints)
  return render_template("private/upload_images.html", images= images,
    interest_points=interest_points, events=events, periods=periods,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

# harvest and clean select EXIF data including datetime, lat, long
@app.route("/admin/upload_images/exif/", methods=['POST', 'GET'])
def getEXIF():
  tags = request.form['key']
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
def image_post():
  # get input from user according to field. Save those values under
  # similar variable names.
  params = dict()
  params["title"] = request.form['title']
  params["img_description"] = request.form['img_description']
  params["latitude"] = utils.safe_float_conv(request.form['latitude'])
  params["longitude"] = utils.safe_float_conv(request.form['longitude'])
  params["period"] = request.form['period']
  month = request.form['month']
  day = request.form['day']
  year = request.form['year']
  params["date_created"] = make_date(month, day, year)
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["edited_by"] = ''
  file = request.files['file']

  # if administrator does not indicate these options
  # for the image, fill field with empty string
  params["interest_point"] = utils.clear_sel(request.form['interest_point'])
  params["event"] = utils.clear_sel(request.form['event'])
  params["period"] = utils.clear_sel(request.form['period'])

  # Addressing the problem of different files with the same filname,
  # This uses the database id past the max database id as a unique value,
  # that cannot be shared by other database rows (hence images),
  # and so there will never be any name conflicts.
  # NOTE: This inuition most likely fails if the server is parrellized in any way
  max_id = database.get_max_img_id()
  this_id = max_id + 1

  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    # If so, make the filename safe by removing unsupported characters
    my_secure_filename = secure_filename(file.filename)
    # prepend unique id to ensure an unique filename
    unique_filename = str(this_id) + '_' + my_secure_filename
    # Move the file from the temporary folder to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    ## Commented out because EXIF is currently extracted in javascript.
    # # Call function to extract EXIF data
    # date_created = getEXIF(app.config['UPLOAD_FOLDER'], filename)
    # Make a thumbnail and store it in the thumbnails directory
    params["thumbnail_name"] = make_thumbnail(unique_filename, this_id)
    params["filename"] = unique_filename
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
  interest_points = database.get_all_rows(schema_livy.InterestPoints)
  points,zones,lines = get_all_feature_collections()
  # get feature types
  feat_types = app.config["FEATURE_TYPES"]
  return render_template("private/upload_ips.html",
    interest_points=interest_points,
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
    feat_types=feat_types,
    **app.config)

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
  # get user input
  params = dict()
  name = params["name"] = request.form['name']
  params["notes"] = request.form['notes']
  params["tags"] = request.form['tags']
  params["books"] = request.form['books']
  color = request.form['color']
  # if administrator does not provide feature_type, fill
  # with empty string
  params["feature_type"] = utils.clear_sel(request.form['feature_type'])
  params["edited_by"] = ''
  # if the administrator provides a geojson object, harvest
  # extra data and supply name and color
  is_gg = bool(request.form['geojson'])
  geo_obj = request.form['geojson'] if is_gg else ''
  params["coordinates"] = str(get_coords(geo_obj))  if is_gg else ''
  params["geojson_feature_type"] = str(get_type(geo_obj)) if is_gg else ''
  params["geojson_object"] = add_name_and_color(geo_obj, name, color) if is_gg else ''

  # insert new db entry
  database.add_to_table(schema_livy.InterestPoints, params)
  return redirect(url_for('index'))

###
###
### Views to search for and delete images ###
@app.route("/admin/delete_images/", methods=["GET"])
def delete_images():
  # get search fields
  fields = get_fields('images')
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get images from search
  if search_term is None:
    images = database.get_all_rows(schema_livy.Images)
  else:
    images = database.search_text(schema_livy.Images, search_field, search_term)
  return render_template("private/delete_images.html", fields=fields, images=images,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/delete_images/delete/", methods=["POST"])
def delete_images_delete():
  keys = request.form.getlist('primary_key')
  database.delete(keys, schema_livy.Images)
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
    interest_points = database.get_all_rows(schema_livy.InterestPoints)
  else:
    interest_points = database.search_text(schema_livy.InterestPoints, search_field, search_term)
  return render_template("private/delete_ips.html", fields=fields,
    interest_points=interest_points)

@app.route("/admin/delete_ips/delete/", methods=["POST"])
def delete_ips_delete():
  # delete selected items from specified table by primary key
  database.delete(request.form.getlist('primary_key'), schema_livy.InterestPoints)
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
    image = database.get_row_by_id(schema_livy.Images,request.args.get('edit-btn'))
    date_created = image['date_created']
    date_created = clean_date(date_created)
    year = date_created[0]
    month = date_created[1]
    day = date_created[2]
    events = database.get_all_rows(schema_livy.Events)
    interest_points = database.get_all_rows(schema_livy.InterestPoints)

    # get periods
    periods = app.config['PERIODS']

    return render_template("private/complete_form_images.html", image=[image],
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
    images = database.get_all_rows(schema_livy.Images)
  else:
    images = database.search_text(schema_livy.Images, search_field, search_term)
  return render_template("private/edit_images.html",
    fields=fields, images=images,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/edit_images/edit/", methods=["POST"])
def edit_images_edit():
  # get new input from user to substitute for old content
  params = dict()
  params["title"] = request.form['title']
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
  image = database.get_row_by_id(schema_livy.Images, key)
  params["created_at"] = image['created_at']
  params["thumbnail_name"] = image['thumbnail_name']
  params["filename"] = image['filename']

  # edit db entry
  database.edit_table_key(schema_livy.Images,key,params)
  return redirect(url_for('index'))

###
###
### Views to edit interest points ###
@app.route("/admin/edit_ips_form/", methods=["GET"])
def edit_ips_form():
  feat_types = app.config['FEATURE_TYPES']
  # if administrator clicks edit button on an interest point
  interest_point = database.get_row_by_id(schema_livy.InterestPoints, request.args.get('edit-btn'))
  return render_template("private/form_ips.html", feat_types=feat_types,
    interest_point=interest_point)


###
###
### Views to search interest points
@app.route("/admin/edit_ips/", methods=["GET"])
def edit_ips():
  table_name = 'interest_points'

  # get search fields
  fields = get_fields(table_name)
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # get interest points from search
  if search_term is None:
    interest_points = database.get_all_rows(schema_livy.InterestPoints)
  else:
    interest_points = database.search_text(schema_livy.InterestPoints, search_field, search_term)

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
  ip = database.get_row_by_id(schema_livy.InterestPoints,  key)
  params["created_at"] = ip['created_at']
  params["geojson_feature_type"] = ip['geojson_feature_type']

  # edit db entry
  database.edit_table_key(schema_livy.InterestPoints,key,params)
  return redirect(url_for('index'))
