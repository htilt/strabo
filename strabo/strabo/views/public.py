import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil
from strabo import app
from strabo import database
from strabo import schema
from strabo.geojson_wrapper import get_all_feature_collections
from strabo.utils import prettify_columns, get_raw_column
import copy

#@app.route("/")
@app.route("/map")
def map():
  template = "public/map.html"
  points,zones,lines = get_all_feature_collections()
  return render_template(template,
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
     **app.config)
'''
@app.route('/map/post', methods=["POST"])
def map_post():
  # get the ip_value user has clicked
  ip_value = request.form.get('name')
  # query db for corresponding images, text
  images = database.search('images', 'interest_point', ip_value, 6)
  text = database.search('text_selections', 'interest_point', ip_value)
  ip_info = {
    'images': images,
    'text-selection': text
  }
  return jsonify(ip_info)'''

@app.route("/about")
def about():
  return render_template("public/about.html",**app.config)
