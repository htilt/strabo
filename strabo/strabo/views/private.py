import os, ast, sys
from contextlib import closing
from strabo import utils
from strabo.geojson_wrapper import get_all_feature_collections

from flask import request, render_template, redirect, url_for

from strabo import database
from strabo import post_helper
from strabo import schema
from strabo import app
# Landing page allows viewer to select amoung tabs to start editing
@app.route("/admin/", methods=["GET"])
def index():
  return render_template("private/base.html",**app.config)

###
###
### Views to upload images to db
@app.route("/admin/upload_images/")
def upload_images():
  interest_points = database.get_all_rows(schema.InterestPoints)
  return render_template("private/upload_images.html",
    interest_points=interest_points,
    **app.config)

@app.route("/admin/upload_images/post", methods=["POST"])
def image_post():
    print(request.form)
    img_obj = post_helper.make_image(request.files['file'],request.form['interest_point'])
    database.store_item(img_obj)
    return redirect(url_for('index'))

###
###
### Views to add interest points to the db
@app.route("/admin/upload_ips/")
def upload_ips():
  points,zones,lines = get_all_feature_collections()
  return render_template("private/upload_ips.html",
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
    **app.config)

@app.route("/admin/interest_points/post", methods=["POST"])
def interest_points_post():
    ip = post_helper.make_interest_point(request.form['title'],request.form['description'],request.form['geojson'],request.form['layer'])
    database.store_item(ip)
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
    images = database.get_all_rows(schema.Images)
  else:
    images = database.search_text(schema.Images, search_field, search_term)
  return render_template("private/delete_images.html", fields=fields, images=images,
    NEW_DATA_DIRECTORY_RELPATH=app.config['NEW_DATA_DIRECTORY_RELPATH'])

@app.route("/admin/delete_images/delete/", methods=["POST"])
def delete_images_delete():
  keys = request.form.getlist('primary_key')
  database.delete(keys, schema.Images)
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
    interest_points = database.get_all_rows(schema.InterestPoints)
  else:
    interest_points = database.search_text(schema.InterestPoints, search_field, search_term)
  return render_template("private/delete_ips.html", fields=fields,
    interest_points=interest_points)

@app.route("/admin/delete_ips/delete/", methods=["POST"])
def delete_ips_delete():
  # delete selected items from specified table by primary key
  database.delete(request.form.getlist('primary_key'), schema.InterestPoints)
  return redirect(url_for('index'))
