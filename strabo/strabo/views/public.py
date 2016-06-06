import os
from flask import request, render_template, url_for, redirect, session, jsonify
from math import ceil
from strabo import app
from strabo import database
from strabo import schema
from strabo.geojson_wrapper import get_all_feature_collections
from strabo.utils import prettify_columns, get_raw_column
import copy
from strabo import public_helper
import werkzeug


@app.route("/")
@app.route("/map")
def map():
  template = "public/map.html"
  points,zones,lines = get_all_feature_collections()
  return render_template(template,
    interest_points_json=points,
    interest_zones_json=lines,
    interest_lines_json=zones,
     **app.config)

@app.route('/map/post', methods=["POST"])
def map_post():
  # get the ip_value user has clicked
  ip_id = request.form['db_id']
  ip = schema.InterestPoints.query.get(ip_id)

  images = ip.images
  ip_info = {
    "db_id": ip_id
  }
  return jsonify(ip_info)

class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/ip_display-<ip_id>/')
def gal_upload(ip_id):
    ip = schema.InterestPoints.query.get(int(ip_id))

    filenames = [img.filename for img in ip.images]
    return render_template("public/ip_show.html",filenames=filenames,**app.config)


@app.route("/about")
def about():
  return render_template("public/about.html",**app.config)
