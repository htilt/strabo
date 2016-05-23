import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil

from strabo import app
from strabo.database import get_flex, get_column_names, \
get_geojson, search, gallery_search
from strabo.geojson import make_geojsons
from strabo.utils import prettify_columns, get_raw_column
import copy

@app.route("/map")
def map():
  template = os.path.join("public/", app.config['MAP_TEMPLATE'])
  points,zones,lines = make_geojsons()
  return render_template(template,
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
     **app.config)

@app.route('/map/post', methods=["POST", "GET"])
def map_post():
  # get the ip_value user has clicked
  ip_value = request.form.get('name')
  # query db for corresponding images, text
  images = search('images', 'interest_point', ip_value, 6)
  text = search('text_selections', 'interest_point', ip_value)
  ip_info = {
    'images': images,
    'text-selection': text
  }
  return jsonify(ip_info)

@app.route("/gallery", methods=["GET"])
def gallery():
  # get search fields
  fields = prettify_columns(app.config['SEARCH_COLUMNS'])
  # get user input for search
  search_term, search_field = request.args.get('search_term'), request.args.get('search_field')
  # if the specified column name is 'prettified', refert to raw column name
  search_field = get_raw_column(search_field)

  # if no search has been performed, show all images
  if search_term == '' or search_term == None:
    images = get_flex('images')
  # or search in all fields
  elif search_field == 'All Fields':
    images = gallery_search('images', search_term, None)
  # or search in specific field
  else:
    images = gallery_search('images', search_term, search_field)
  return render_template("public/gallery.html", images=images,
    fields=fields,**app.config)

@app.route("/timeline")
def timeline():
  table_name = 'events'
  events = get_flex(table_name, 100)
  return render_template("public/under_construction.html",**app.config)
  # return render_template("public/timeline.html", events=events,**app.config)

@app.route("/about")
def about():
  return render_template("public/about.html",**app.config)
